# GraphDoc - Knowledge Graph Enhanced Document Processing

GraphDoc (GraphRAG) is a document analysis and retrieval system that enhances traditional Retrieval-Augmented Generation (RAG) with knowledge graph capabilities. It's designed to process, index, and query complex document collections by combining vector-based retrieval with graph relationship context.

## Features

- **Document Processing**: Extract structured text from PDFs, text files, and other document formats
- **Knowledge Graph Construction**: Automatically extract entities and relationships
- **Timeline Analysis**: Create chronological sequences of events from documents
- **Graph-based Retrieval**: Enhance document retrieval with graph relationships
- **Batch Processing**: Process large document collections efficiently

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[test]"
```

## Quick Start

### Python API

```python
from graphrag_doc.index.batch_indexer import GraphRAGIndexer

# Initialize the indexer
indexer = GraphRAGIndexer(working_dir="graphrag_index")

# Process documents
results = indexer.index_documents(
    folder_path="path/to/documents",
    file_extensions=[".txt", ".pdf", ".docx", ".md"],
    recursive=True,
    extract_metadata=True
)

# Print indexing results
for result in results:
    print(f"{result.filename}: {result.status} - {result.message}")

# Access document metadata
for result in results:
    if result.status == "Success" and result.metadata:
        print(f"File: {result.filename}")
        print(f"Size: {result.metadata.file_size_bytes} bytes")
        print(f"Word count: {result.metadata.word_count}")
        
        # For PDFs, additional metadata may be available
        if result.metadata.num_pages:
            print(f"Pages: {result.metadata.num_pages}")

# Use the indexed documents with the LightRAG query API
from lightrag import QueryParam
response = indexer.rag.query(
    "When did the event occur?",
    param=QueryParam(mode="mix")
)
print(response)
```

### Advanced Indexing Options

```python
# Process specific file types
indexer.index_documents(
    folder_path="path/to/documents",
    file_extensions=[".pdf"],  # Only process PDF files
    recursive=True
)

# Non-recursive search (only files in the specified folder, not subfolders)
indexer.index_documents(
    folder_path="path/to/documents",
    recursive=False
)

# Skip metadata extraction for faster processing
indexer.index_documents(
    folder_path="path/to/documents",
    extract_metadata=False
)

# Customize batch size during initialization
indexer = GraphRAGIndexer(
    working_dir="graphrag_index",
    batch_size=50  # Process 50 documents per batch
)
```

### Command Line Interface

Index documents using the CLI:

```bash
# Basic usage
python -m graphrag_doc.sdk.cli index path/to/documents

# Specify working directory and output file
python -m graphrag_doc.sdk.cli index path/to/documents --working-dir=my_index --output=results.json

# Specify file types
python -m graphrag_doc.sdk.cli index path/to/documents --file-types=".txt,.pdf,.docx,.md"

# Set batch size
python -m graphrag_doc.sdk.cli index path/to/documents --batch-size=50
```

### Sample Script

The project includes a sample script for batch document processing:

```bash
python -m src.scripts.index_sample_documents path/to/documents --working-dir=my_index --output=results.json
```

## Supported File Formats

- Text files (`.txt`)
- PDF documents (`.pdf`) - requires PyPDF2
- Word documents (`.docx`) - requires python-docx
- Markdown files (`.md`)
- Other formats with textract (optional)

## Configuration

GraphDoc uses environment variables for configuration:

- `GRAPHDOC_NEO4J_URI`: Neo4j database URI (default: bolt://localhost:7687)
- `GRAPHDOC_NEO4J_USERNAME`: Neo4j username
- `GRAPHDOC_NEO4J_PASSWORD`: Neo4j password
- `OPENAI_API_KEY`: OpenAI API key
- `GRAPHDOC_OPENAI_MODEL`: OpenAI model to use (default: gpt-4o-mini)
- `GRAPHDOC_INDEX_DIR`: Path to store indexes (default: graphrag_index)

## Development

### Running Tests

```bash
pytest
```

Run a single test:

```bash
pytest tests/path_to_test.py::test_function_name
```

Run the indexer tests:

```bash
pytest tests/test_indexer.py
```

### Code Style

```bash
flake8
pyright
```

## License

MIT