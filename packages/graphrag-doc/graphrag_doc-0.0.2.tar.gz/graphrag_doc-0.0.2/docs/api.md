# GraphRAG SDK API Documentation

This document provides the API reference for the GraphRAG document indexing SDK.

## Table of Contents

- [Installation](#installation)
- [GraphRAGIndexer](#graphragindexer)
  - [Constructor](#constructor)
  - [Methods](#methods)
- [CLI Interface](#cli-interface)
  - [Command-Line Options](#command-line-options)
  - [Examples](#examples)
- [Models](#models)
  - [DocumentMetadata](#documentmetadata)
  - [DocumentIndexResult](#documentindexresult)
- [Examples](#examples-1)
  - [Basic Usage](#basic-usage)
  - [Processing Specific File Types](#processing-specific-file-types)
  - [Advanced Configuration](#advanced-configuration)

## Installation

```bash
# Install from PyPI
pip install graphrag-doc

# Install from source
pip install -e .
```

## GraphRAGIndexer

The main class for batch processing and indexing documents.

### Constructor

```python
GraphRAGIndexer(working_dir="graphrag_index", batch_size=20)
```

**Parameters:**
- `working_dir` (str): Directory to store indexed data
- `batch_size` (int): Number of documents to process in each batch

### Methods

#### `index_documents`

Indexes all specified document types in the given folder.

```python
indexer.index_documents(
    folder_path, 
    file_extensions=None,  # Default: ['.txt', '.pdf', '.docx', '.md']
    recursive=True, 
    extract_metadata=True
)
```

**Parameters:**
- `folder_path` (str): Path to the folder containing documents
- `file_extensions` (List[str], optional): List of file extensions to process
- `recursive` (bool): Whether to search subdirectories
- `extract_metadata` (bool): Whether to extract and store document metadata

**Returns:**
- List[DocumentIndexResult]: Results of the indexing operation

#### `find_matching_files`

Finds files matching the specified extensions in a folder.

```python
indexer.find_matching_files(folder_path, file_extensions, recursive)
```

**Parameters:**
- `folder_path` (str): Path to search for files
- `file_extensions` (List[str]): File extensions to match
- `recursive` (bool): Whether to search subdirectories

**Returns:**
- List[str]: List of matching file paths

#### `extract_text_from_file`

Extracts text and metadata from a file based on its extension.

```python
indexer.extract_text_from_file(file_path)
```

**Parameters:**
- `file_path` (str): Path to the file

**Returns:**
- Tuple[Optional[str], Dict[str, Any]]: Extracted text and metadata

#### `save_metadata_to_json`

Saves metadata dictionary to a JSON file.

```python
indexer.save_metadata_to_json(metadata_dict, output_path)
```

**Parameters:**
- `metadata_dict` (Dict[str, DocumentMetadata]): Mapping of filenames to metadata
- `output_path` (str): Path to save the JSON file

## CLI Interface

The GraphRAG SDK provides a command-line interface for batch indexing operations.

### Command-Line Options

```
python -m graphrag_doc.sdk.cli index [OPTIONS] FOLDER_PATH
```

**Arguments:**
- `FOLDER_PATH`: Path to the folder containing documents to index

**Options:**
- `--working-dir TEXT`: Directory for storing indexed data (default: "graphrag_index")
- `--output TEXT`: Path to save indexing results as a JSON file
- `--file-types TEXT`: Comma-separated list of file extensions to index (default: ".txt,.pdf,.docx,.md")
- `--batch-size INTEGER`: Number of documents to process in each batch (default: 20)
- `--recursive / --no-recursive`: Whether to recursively search for files in subdirectories (default: True)
- `--extract-metadata / --no-metadata`: Whether to extract metadata from documents (default: True)
- `--max-workers INTEGER`: Maximum number of worker threads for parallel processing (default: auto)

### Examples

```bash
# Basic usage
python -m graphrag_doc.sdk.cli index ./documents

# Specify working directory and output file
python -m graphrag_doc.sdk.cli index ./documents --working-dir=my_index --output=results.json

# Index only specific file types
python -m graphrag_doc.sdk.cli index ./documents --file-types=.txt,.md

# Non-recursive indexing
python -m graphrag_doc.sdk.cli index ./documents --no-recursive
```

## Models

### DocumentMetadata

Contains metadata extracted from a document.

**Fields:**
- `filename` (str): Name of the document file
- `file_path` (str): Full path to the document file
- `file_size_bytes` (int): Size of the file in bytes
- `file_extension` (str): File extension
- `creation_time` (Optional[str]): File creation timestamp
- `modification_time` (Optional[str]): File last modification timestamp
- `num_pages` (Optional[int]): Number of pages (for PDFs)
- `word_count` (Optional[int]): Approximate word count
- `indexed_time` (str): Time when the document was indexed

### DocumentIndexResult

Represents the result of an indexed document.

**Fields:**
- `filename` (str): Name of the indexed document
- `status` (str): Status of indexing (Success/Failed)
- `message` (str): Details about the indexing process
- `processing_time_ms` (Optional[int]): Time taken to process the document in milliseconds
- `metadata` (Optional[DocumentMetadata]): Metadata about the document
- `chunk_count` (Optional[int]): Number of chunks created from the document

## Examples

### Basic Usage

```python
from graphrag_doc.index.batch_indexer import GraphRAGIndexer

# Initialize the indexer
indexer = GraphRAGIndexer(working_dir="graphrag_index")

# Process documents in a folder
results = indexer.index_documents(
    folder_path="path/to/documents"
)

# Print results
for result in results:
    print(f"{result.filename}: {result.status} - {result.message}")
```

### Processing Specific File Types

```python
from graphrag_doc.index.batch_indexer import GraphRAGIndexer

# Initialize the indexer
indexer = GraphRAGIndexer(working_dir="my_index")

# Process only PDF and DOCX files
results = indexer.index_documents(
    folder_path="path/to/documents",
    file_extensions=[".pdf", ".docx"],
    recursive=True
)

# Print successful results
successful = [r for r in results if r.status == "Success"]
print(f"Successfully processed {len(successful)} documents")
```

### Advanced Configuration

```python
from graphrag_doc.index.batch_indexer import GraphRAGIndexer
import json

# Initialize the indexer with custom batch size
indexer = GraphRAGIndexer(
    working_dir="custom_index",
    batch_size=50
)

# Process documents with custom configuration
results = indexer.index_documents(
    folder_path="path/to/documents",
    file_extensions=[".txt", ".md"],
    recursive=True,
    extract_metadata=True
)

# Access metadata
for result in results:
    if result.status == "Success" and result.metadata:
        print(f"File: {result.filename}")
        print(f"Size: {result.metadata.file_size_bytes} bytes")
        print(f"Words: {result.metadata.word_count}")
        print(f"Created: {result.metadata.creation_time}")
        print("---")

# Save results to JSON
with open("indexing_results.json", "w") as f:
    json.dump([r.model_dump() for r in results], f, indent=2)
```