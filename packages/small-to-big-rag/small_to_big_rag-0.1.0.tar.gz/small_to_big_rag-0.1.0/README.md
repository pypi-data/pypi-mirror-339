# Small-to-Big RAG

A Python package implementing the Small-to-Big RAG approach for more effective retrieval augmented generation.

## Installation

```bash
pip install small-to-big-rag
```

## Usage

```python
from small_to_big_rag import SmallToBigRAG
import os

# Initialize with Azure OpenAI credentials
rag = SmallToBigRAG(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-10-21",
    embedding_model="text-embedding-3-small",
    llm_model="gpt-4o-mini"
)

# Load a document
rag.load_file("path/to/document.txt")

# Or load text directly
text = """
Your document text here.
This can be multi-paragraph content.

The system will split this into paragraphs and sentences.
"""
rag.load_text(text)

# Generate a response
response = rag.generate_response(
    query="What is the main topic of the document?",
    system_prompt="You are a helpful assistant specialized in document analysis."
)

# Print the answer
print(response["answer"])

# Access source information
print("\nSources used:")
for i, sentence in enumerate(response["sources"]["sentences"]):
    print(f"Sentence {i+1}: {sentence[:100]}...")

for i, paragraph in enumerate(response["sources"]["paragraphs"]):
    print(f"Paragraph {i+1}: {paragraph[:100]}...")
```

## Features

- Small-to-Big RAG approach that retrieves both sentences and their parent paragraphs
- Maintains relationships between sentences and paragraphs for better context
- Uses ChromaDB for vector storage and retrieval
- Supports Azure OpenAI API
- Easy-to-use Python API

## Requirements

- Python 3.8+
- langchain-text-splitters
- openai
- chromadb
- python-dotenv

## License

MIT