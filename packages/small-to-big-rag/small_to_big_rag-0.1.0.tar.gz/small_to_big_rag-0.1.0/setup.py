from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="small-to-big-rag",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Small-to-Big RAG implementation for more effective retrieval augmented generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WSIB-Innovation/small-to-big-package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain-text-splitters>=0.0.1",
        "openai>=1.0.0",
        "chromadb>=0.4.0",
        "python-dotenv>=1.0.0",
    ],
)