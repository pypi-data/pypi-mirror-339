from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import AzureOpenAI
import os
import chromadb
import re
from typing import Dict, List, Any, Union, Optional
from enum import Enum


class RAGMode(Enum):
    """Enum for different RAG retrieval strategies."""
    SMALL_TO_BIG = "small_to_big"  # Retrieve sentences then expand to paragraphs
    SENTENCES_ONLY = "sentences_only"  # Retrieve only sentences
    PARAGRAPHS_ONLY = "paragraphs_only"  # Retrieve only paragraphs


class SmallToBigRAG:
    """
    Small-to-Big RAG implementation that retrieves both sentence and paragraph level context
    for more effective retrieval augmented generation.
    
    Supports multiple retrieval modes for testing and comparison.
    """
    
    def __init__(
        self,
        api_key: str = None,
        api_version: str = "2024-10-21",
        azure_endpoint: str = None,
        embedding_model: str = "text-embedding-3-small",
        llm_model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        embedding_client = None,
        chroma_client = None,
        chroma_persist_directory: str = None,
        default_rag_mode: RAGMode = RAGMode.SMALL_TO_BIG
    ):
        """
        Initialize the SmallToBigRAG system.
        
        Args:
            api_key: Azure OpenAI API key
            api_version: Azure OpenAI API version
            azure_endpoint: Azure OpenAI endpoint
            embedding_model: Model to use for embeddings
            llm_model: Model to use for generation
            temperature: Temperature for generation
            embedding_client: Custom embedding client (if not using default)
            chroma_client: Custom ChromaDB client (if not using default)
            chroma_persist_directory: Directory to persist ChromaDB data (optional)
            default_rag_mode: Default RAG retrieval strategy to use
        """
        # Set up clients
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.temperature = temperature
        self.default_rag_mode = default_rag_mode
        
        # Initialize embedding client if not provided
        if embedding_client:
            self.client = embedding_client
        else:
            if not api_key or not azure_endpoint:
                raise ValueError("Must provide either an embedding client or API credentials")
            
            self.client = AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint
            )
        
        # Initialize ChromaDB client
        if chroma_client:
            self.chroma_client = chroma_client
        else:
            if chroma_persist_directory:
                self.chroma_client = chromadb.PersistentClient(path=chroma_persist_directory)
            else:
                self.chroma_client = chromadb.Client()
        
        # Store chunks
        self.all_chunks = []
        self.document_loaded = False
        
        # Store statistics for comparison
        self.stats = {
            RAGMode.SMALL_TO_BIG.value: {"queries": 0, "avg_context_size": 0},
            RAGMode.SENTENCES_ONLY.value: {"queries": 0, "avg_context_size": 0},
            RAGMode.PARAGRAPHS_ONLY.value: {"queries": 0, "avg_context_size": 0}
        }
    
    def load_text(self, text: str, reset_collections: bool = True) -> List[Dict[str, Any]]:
        """
        Load and process text into sentence and paragraph chunks
        
        Args:
            text: The document text to process
            reset_collections: Whether to reset existing collections
            
        Returns:
            List of chunk metadata
        """
        # Create text splitters for paragraphs
        paragraph_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n"], is_separator_regex=True
        )
        
        # Split paragraphs
        paragraph_chunks = paragraph_splitter.split_text(text)
        
        # Clean paragraph chunks (remove leading whitespace)
        paragraph_chunks = [p.strip() for p in paragraph_chunks]
        
        sentence_texts = []  # store sentences for embeddings
        all_chunks = []  # store relationships between parent and child chunks
        global_sentence_count = 0
        
        # Process paragraphs and sentences
        for i, paragraph in enumerate(paragraph_chunks):
            # Custom sentence splitting that preserves punctuation with the sentence
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            # Make sure we don't have empty sentences (can happen with multiple spaces after punctuation)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            for j, sentence in enumerate(sentences):
                sentence_texts.append(sentence)
                all_chunks.append({
                    "id": f"p{i}_s{global_sentence_count}",
                    "text": sentence,
                    "parent_id": f"p{i}",
                    "parent_chunk": paragraph,
                    "type": "sentence",
                    "original_paragraph_index": i,
                    "original_sentence_index": global_sentence_count,
                    "paragraph_relative_index": j
                })
                global_sentence_count += 1
                
            all_chunks.append({
                "id": f"p{i}",
                "text": paragraph,
                "parent_id": None,
                "parent_chunk": None,
                "type": "paragraph",
                "original_paragraph_index": i,
            })

        # Generate embeddings
        sentence_embeddings = self.client.embeddings.create(
            input=sentence_texts, model=self.embedding_model
        )
        paragraph_embeddings = self.client.embeddings.create(
            input=paragraph_chunks, model=self.embedding_model
        )

        # Store in ChromaDB - get or create collections
        if reset_collections:
            # Delete collections if they exist
            try:
                self.chroma_client.delete_collection("sentences")
                self.chroma_client.delete_collection("paragraphs")
            except:
                pass
            
        sentence_collection = self.chroma_client.get_or_create_collection(name="sentences")
        paragraph_collection = self.chroma_client.get_or_create_collection(name="paragraphs")
        
        # Store sentences
        sentence_collection.upsert(
            documents=sentence_texts,
            embeddings=[emb.embedding for emb in sentence_embeddings.data],
            ids=[chunk["id"] for chunk in all_chunks if chunk["type"] == "sentence"],
            metadatas=[{
                "parent_id": chunk["parent_id"],
                "original_paragraph_index": chunk["original_paragraph_index"],
                "original_sentence_index": chunk["original_sentence_index"],
                "paragraph_relative_index": chunk["paragraph_relative_index"]
            } for chunk in all_chunks if chunk["type"] == "sentence"]
        )

        # Store paragraphs
        paragraph_collection.upsert(
            documents=paragraph_chunks,
            embeddings=[emb.embedding for emb in paragraph_embeddings.data],
            ids=[chunk["id"] for chunk in all_chunks if chunk["type"] == "paragraph"],
            metadatas=[{
                "original_paragraph_index": chunk["original_paragraph_index"]
            } for chunk in all_chunks if chunk["type"] == "paragraph"]
        )

        self.all_chunks = all_chunks
        self.document_loaded = True
        
        return all_chunks
    
    def load_file(self, file_path: str, reset_collections: bool = True) -> List[Dict[str, Any]]:
        """
        Load and process a document file into sentence and paragraph chunks
        
        Args:
            file_path: Path to the document file
            reset_collections: Whether to reset existing collections
            
        Returns:
            List of chunk metadata
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return self.load_text(text, reset_collections)
    
    def query_small_to_big(self, query_text: str, k_sentences: int = 5, k_paragraphs: int = 3) -> Dict[str, Any]:
        """
        Query using small-to-big approach: retrieve sentences then expand to their parent paragraphs.
        
        Args:
            query_text: The query text
            k_sentences: Number of sentences to retrieve
            k_paragraphs: Maximum number of unique paragraphs to include (from sentence parents)
            
        Returns:
            Dictionary containing query results with both sentence and paragraph context
        """
        if not self.document_loaded:
            raise ValueError("No document has been loaded. Call load_text() or load_file() first.")
            
        # Generate embedding for the query
        query_embedding = self.client.embeddings.create(
            input=query_text, model=self.embedding_model
        ).data[0].embedding
        
        # Retrieve the most similar sentences
        sentence_collection = self.chroma_client.get_collection(name="sentences")
        sentence_results = sentence_collection.query(
            query_embeddings=query_embedding, n_results=k_sentences
        )
        
        # Get parent paragraphs
        parent_ids = list(set([meta["parent_id"] for meta in sentence_results["metadatas"][0]]))
        # Limit to k_paragraphs if needed
        parent_ids = parent_ids[:k_paragraphs]
        
        parent_paragraphs = [
            next((chunk for chunk in self.all_chunks if chunk["id"] == parent_id), None) 
            for parent_id in parent_ids
        ]
        parent_paragraphs = [p for p in parent_paragraphs if p]  # Remove None values
        
        # Build context
        sentence_context = "\n\n".join([f"Sentence: {doc}" for doc in sentence_results["documents"][0]])
        paragraph_context = "\n\n".join([f"Paragraph: {p['text']}" for p in parent_paragraphs])
        
        # Create enhanced sentence metadata
        sentence_metadata = []
        for i, metadata in enumerate(sentence_results["metadatas"][0]):
            parent_id = metadata["parent_id"]
            parent_index = next((idx for idx, p in enumerate(parent_paragraphs) if p["id"] == parent_id), None)
            
            sentence_metadata.append({
                "id": sentence_results["ids"][0][i],
                "parent_id": parent_id,
                "parent_index": parent_index,
                "original_paragraph_index": metadata["original_paragraph_index"],
                "original_sentence_index": metadata["original_sentence_index"],
                "paragraph_relative_index": metadata["paragraph_relative_index"]
            })
        
        # Calculate context size for statistics
        context_size = sum(len(s) for s in sentence_results["documents"][0]) + sum(len(p["text"]) for p in parent_paragraphs)
        self._update_stats(RAGMode.SMALL_TO_BIG.value, context_size)
        
        return {
            "sentences": sentence_results,
            "paragraphs": parent_paragraphs,
            "sentence_metadata": sentence_metadata,
            "context": f"Relevant Sentences:\n{sentence_context}\n\nRelevant Paragraphs:\n{paragraph_context}"
        }
    
    def query_sentences_only(self, query_text: str, k_sentences: int = 5) -> Dict[str, Any]:
        """
        Query using sentences-only approach: retrieve only sentences without expanding to paragraphs.
        
        Args:
            query_text: The query text
            k_sentences: Number of sentences to retrieve
            
        Returns:
            Dictionary containing query results with only sentence context
        """
        if not self.document_loaded:
            raise ValueError("No document has been loaded. Call load_text() or load_file() first.")
            
        # Generate embedding for the query
        query_embedding = self.client.embeddings.create(
            input=query_text, model=self.embedding_model
        ).data[0].embedding
        
        # Retrieve the most similar sentences
        sentence_collection = self.chroma_client.get_collection(name="sentences")
        sentence_results = sentence_collection.query(
            query_embeddings=query_embedding, n_results=k_sentences
        )
        
        # Build context
        sentence_context = "\n\n".join([f"Sentence: {doc}" for doc in sentence_results["documents"][0]])
        
        # Create basic sentence metadata
        sentence_metadata = []
        for i, metadata in enumerate(sentence_results["metadatas"][0]):
            sentence_metadata.append({
                "id": sentence_results["ids"][0][i],
                "parent_id": metadata["parent_id"],
                "parent_index": None,
                "original_paragraph_index": metadata["original_paragraph_index"],
                "original_sentence_index": metadata["original_sentence_index"],
                "paragraph_relative_index": metadata["paragraph_relative_index"]
            })
        
        # Calculate context size for statistics
        context_size = sum(len(s) for s in sentence_results["documents"][0])
        self._update_stats(RAGMode.SENTENCES_ONLY.value, context_size)
        
        return {
            "sentences": sentence_results,
            "paragraphs": [],
            "sentence_metadata": sentence_metadata,
            "context": f"Relevant Sentences:\n{sentence_context}"
        }
    
    def query_paragraphs_only(self, query_text: str, k_paragraphs: int = 3) -> Dict[str, Any]:
        """
        Query using paragraphs-only approach: retrieve only paragraphs without sentence-level search.
        
        Args:
            query_text: The query text
            k_paragraphs: Number of paragraphs to retrieve
            
        Returns:
            Dictionary containing query results with only paragraph context
        """
        if not self.document_loaded:
            raise ValueError("No document has been loaded. Call load_text() or load_file() first.")
            
        # Generate embedding for the query
        query_embedding = self.client.embeddings.create(
            input=query_text, model=self.embedding_model
        ).data[0].embedding
        
        # Retrieve the most similar paragraphs
        paragraph_collection = self.chroma_client.get_collection(name="paragraphs")
        paragraph_results = paragraph_collection.query(
            query_embeddings=query_embedding, n_results=k_paragraphs
        )
        
        # Build list of paragraph chunks from results
        paragraphs = []
        for i, para_id in enumerate(paragraph_results["ids"][0]):
            paragraph = next((chunk for chunk in self.all_chunks if chunk["id"] == para_id), None)
            if paragraph:
                paragraphs.append(paragraph)
        
        # Build context
        paragraph_context = "\n\n".join([f"Paragraph: {p['text']}" for p in paragraphs])
        
        # Calculate context size for statistics
        context_size = sum(len(p["text"]) for p in paragraphs)
        self._update_stats(RAGMode.PARAGRAPHS_ONLY.value, context_size)
        
        return {
            "sentences": {"documents": [[]], "ids": [[]], "metadatas": [[]]},  # Empty sentence results
            "paragraphs": paragraphs,
            "sentence_metadata": [],
            "context": f"Relevant Paragraphs:\n{paragraph_context}"
        }
    
    def query(self, query_text: str, mode: RAGMode = None, k_sentences: int = 5, k_paragraphs: int = 3) -> Dict[str, Any]:
        """
        Query the RAG system using the specified retrieval strategy.
        
        Args:
            query_text: The query text
            mode: RAG retrieval strategy to use (defaults to the one set during initialization)
            k_sentences: Number of sentences to retrieve
            k_paragraphs: Number of paragraphs to retrieve
            
        Returns:
            Dictionary containing query results
        """
        if mode is None:
            mode = self.default_rag_mode
            
        if mode == RAGMode.SMALL_TO_BIG:
            return self.query_small_to_big(query_text, k_sentences, k_paragraphs)
        elif mode == RAGMode.SENTENCES_ONLY:
            return self.query_sentences_only(query_text, k_sentences)
        elif mode == RAGMode.PARAGRAPHS_ONLY:
            return self.query_paragraphs_only(query_text, k_paragraphs)
        else:
            raise ValueError(f"Unknown RAG mode: {mode}")
    
    def generate_response(
        self, 
        query: str, 
        mode: RAGMode = None,
        system_prompt: str = "You are a helpful assistant.", 
        k_sentences: int = 5, 
        k_paragraphs: int = 3
    ) -> Dict[str, Any]:
        """
        Generate a response to a query using the specified RAG strategy
        
        Args:
            query: The query text
            mode: RAG retrieval strategy to use (defaults to the one set during initialization)
            system_prompt: The system prompt for the LLM
            k_sentences: Number of sentences to retrieve
            k_paragraphs: Number of paragraphs to retrieve
            
        Returns:
            Dictionary containing response and source information
        """
        # Get RAG results
        rag_results = self.query(query, mode, k_sentences, k_paragraphs)
        
        # Generate response
        messages = [
            {"role": "system", "content": system_prompt + " Use the following context to answer the user's question. If the information to answer is not available in the context, state that clearly."},
            {"role": "user", "content": f"Context:\n{rag_results['context']}\n\nQuestion: {query}"}
        ]
        
        response = self.client.chat.completions.create(
            model=self.llm_model, messages=messages, temperature=self.temperature
        )
        
        # Return mode used for this query in the response
        mode_value = mode.value if mode else self.default_rag_mode.value
        
        return {
            "answer": response.choices[0].message.content,
            "mode": mode_value,
            "sources": {
                "sentences": rag_results.get("sentences", {}).get("documents", [[]])[0],
                "paragraphs": [p["text"] for p in rag_results.get("paragraphs", [])],
                "sentence_metadata": rag_results.get("sentence_metadata", []),
                "paragraph_metadata": [{"original_paragraph_index": p["original_paragraph_index"]} for p in rag_results.get("paragraphs", [])]
            }
        }
    
    def _update_stats(self, mode: str, context_size: int) -> None:
        """Update statistics for the given mode"""
        stats = self.stats[mode]
        stats["queries"] += 1
        # Update running average of context size
        stats["avg_context_size"] = (
            (stats["avg_context_size"] * (stats["queries"] - 1) + context_size) / stats["queries"]
        )
    
    def get_stats(self) -> Dict[str, Dict[str, float]]:
        """Get usage statistics for different RAG modes"""
        return self.stats
    
    def compare_rag_modes(self, queries: List[str], system_prompt: str = "You are a helpful assistant.") -> Dict[str, List[Dict[str, Any]]]:
        """
        Compare different RAG modes on the same set of queries
        
        Args:
            queries: List of query strings to test
            system_prompt: System prompt to use for all queries
            
        Returns:
            Dictionary with results for each mode
        """
        results = {
            RAGMode.SMALL_TO_BIG.value: [],
            RAGMode.SENTENCES_ONLY.value: [],
            RAGMode.PARAGRAPHS_ONLY.value: []
        }
        
        for query in queries:
            # Test each mode with the same query
            for mode in RAGMode:
                response = self.generate_response(
                    query=query,
                    mode=mode,
                    system_prompt=system_prompt
                )
                results[mode.value].append({
                    "query": query,
                    "answer": response["answer"],
                    "context_size": sum(len(s) for s in response["sources"]["sentences"]) + 
                                    sum(len(p) for p in response["sources"]["paragraphs"])
                })
        
        return results