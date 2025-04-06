import os
import json
import tempfile
import pytest
from pathlib import Path
from typing import Dict, Any

from graphrag_doc.index.batch_indexer import (
    GraphRAGIndexer, 
    DocumentIndexResult, 
    DocumentMetadata,
    ExtractedMetadata
)


# Test data
TEST_TEXT = """This is a test document.
It has multiple lines.
We're using it to test the indexer."""

TEST_PDF_CONTENT = """This is sample PDF content
for testing the PDF extraction.
The indexer should parse this correctly."""


@pytest.fixture
def test_folder():
    """Create a temporary test folder with sample documents."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a text file
        with open(os.path.join(tmpdir, "sample1.txt"), "w", encoding="utf-8") as f:
            f.write(TEST_TEXT)
        
        # Create a markdown file
        with open(os.path.join(tmpdir, "sample2.md"), "w", encoding="utf-8") as f:
            f.write("# Test Markdown\n\n" + TEST_TEXT)
        
        # Create a subdirectory
        subdir = os.path.join(tmpdir, "subdir")
        os.makedirs(subdir, exist_ok=True)
        
        # Create another text file in the subdirectory
        with open(os.path.join(subdir, "sample3.txt"), "w", encoding="utf-8") as f:
            f.write("This is a document in a subdirectory.\n" + TEST_TEXT)
        
        yield tmpdir


@pytest.fixture
def working_dir():
    """Create a temporary working directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_indexer_initialization():
    """Test that the indexer initializes correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        indexer = GraphRAGIndexer(working_dir=tmpdir)
        assert indexer is not None
        assert indexer.working_dir == tmpdir
        assert indexer.batch_size == 20


def test_extract_text_from_file_txt():
    """Test text extraction from a text file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        indexer = GraphRAGIndexer(working_dir=tmpdir)
        file_path = os.path.join(tmpdir, "test.txt")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(TEST_TEXT)
        
        text, metadata = indexer.extract_text_from_file(file_path)
        assert text == TEST_TEXT
        assert "word_count" in metadata
        assert metadata["word_count"] == len(TEST_TEXT.split())


def test_find_matching_files(test_folder):
    """Test finding files matching specified extensions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        indexer = GraphRAGIndexer(working_dir=tmpdir)
        
        # Test with recursive=True
        recursive_files = indexer.find_matching_files(
            test_folder,
            [".txt", ".md"],
            True
        )
        assert len(recursive_files) == 3
        
        # Test with recursive=False
        non_recursive_files = indexer.find_matching_files(
            test_folder,
            [".txt", ".md"],
            False
        )
        assert len(non_recursive_files) == 2
        
        # Test with only .txt extension
        txt_files = indexer.find_matching_files(
            test_folder,
            [".txt"],
            True
        )
        assert len(txt_files) == 2
        
        # Test with only .md extension
        md_files = indexer.find_matching_files(
            test_folder,
            [".md"],
            True
        )
        assert len(md_files) == 1


def test_get_file_metadata():
    """Test file metadata extraction."""
    with tempfile.TemporaryDirectory() as tmpdir:
        indexer = GraphRAGIndexer(working_dir=tmpdir)
        
        # Create a test file
        file_path = os.path.join(tmpdir, "metadata_test.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(TEST_TEXT)
        
        # Create test metadata
        extracted_metadata: ExtractedMetadata = {
            "word_count": 16,
            "num_pages": 1
        }
        
        # Get metadata
        metadata = indexer.get_file_metadata(file_path, extracted_metadata)
        
        # Check metadata fields
        assert isinstance(metadata, DocumentMetadata)
        assert metadata.filename == "metadata_test.txt"
        assert metadata.file_path == str(Path(file_path).absolute())
        assert metadata.file_extension == ".txt"
        assert metadata.file_size_bytes > 0
        assert metadata.creation_time is not None
        assert metadata.modification_time is not None
        assert metadata.indexed_time is not None
        assert metadata.word_count == 16
        assert metadata.num_pages == 1


def test_process_file_safely():
    """Test safe processing of a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        indexer = GraphRAGIndexer(working_dir=tmpdir)
        
        # Create a test file
        file_path = os.path.join(tmpdir, "process_test.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(TEST_TEXT)
        
        # Process the file
        text, result = indexer._process_file_safely(file_path)
        
        # Check result
        assert text is not None
        assert text.startswith("File: process_test.txt")
        assert TEST_TEXT in text
        assert result.status == "Success"
        assert result.filename == "process_test.txt"
        assert result.processing_time_ms is not None
        assert result.processing_time_ms > 0
        
        # Test with a non-existent file
        non_existent_path = os.path.join(tmpdir, "non_existent.txt")
        text, result = indexer._process_file_safely(non_existent_path)
        
        # Check error result
        assert text is None
        assert result.status == "Failed"
        assert "non_existent.txt" in result.filename
        assert result.processing_time_ms is not None


def test_save_metadata_to_json():
    """Test saving metadata to JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        indexer = GraphRAGIndexer(working_dir=tmpdir)
        
        # Create test metadata
        metadata1 = DocumentMetadata(
            filename="file1.txt",
            file_path="/path/to/file1.txt",
            file_size_bytes=100,
            file_extension=".txt",
            creation_time="2023-01-01T00:00:00",
            modification_time="2023-01-02T00:00:00",
            indexed_time="2023-01-03T00:00:00",
            word_count=50
        )
        
        metadata2 = DocumentMetadata(
            filename="file2.pdf",
            file_path="/path/to/file2.pdf",
            file_size_bytes=200,
            file_extension=".pdf",
            creation_time="2023-02-01T00:00:00",
            modification_time="2023-02-02T00:00:00",
            indexed_time="2023-02-03T00:00:00",
            word_count=100,
            num_pages=5
        )
        
        # Create metadata dictionary
        metadata_dict = {
            "file1.txt": metadata1,
            "file2.pdf": metadata2
        }
        
        # Save metadata to JSON
        output_path = os.path.join(tmpdir, "metadata.json")
        indexer.save_metadata_to_json(metadata_dict, output_path)
        
        # Check that the file exists
        assert os.path.exists(output_path)
        
        # Read the JSON file
        with open(output_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        
        # Check that the data is correct
        assert len(loaded_data) == 2
        assert "file1.txt" in loaded_data
        assert "file2.pdf" in loaded_data
        assert loaded_data["file1.txt"]["word_count"] == 50
        assert loaded_data["file2.pdf"]["num_pages"] == 5


def test_index_documents(test_folder, working_dir):
    """Test indexing a folder of documents."""
    # Initialize indexer
    indexer = GraphRAGIndexer(working_dir=working_dir)
    
    # Run indexing
    results = indexer.index_documents(
        folder_path=test_folder,
        file_extensions=[".txt", ".md"],
        recursive=True,
        extract_metadata=True
    )
    
    # Verify results
    assert len(results) == 3  # Should have 3 documents
    assert all(isinstance(r, DocumentIndexResult) for r in results)
    assert all(r.status == "Success" for r in results)
    
    # Check that metadata was saved
    metadata_path = os.path.join(working_dir, "document_metadata.json")
    assert os.path.exists(metadata_path)
    
    # Verify metadata content
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
        assert len(metadata) == 3
        
        # Check that each file has metadata
        filenames = ["sample1.txt", "sample2.md", "sample3.txt"]
        for filename in filenames:
            assert any(filename in key for key in metadata.keys())


def test_non_recursive_indexing(test_folder, working_dir):
    """Test non-recursive indexing."""
    # Initialize indexer
    indexer = GraphRAGIndexer(working_dir=working_dir)
    
    # Run indexing without recursion
    results = indexer.index_documents(
        folder_path=test_folder,
        file_extensions=[".txt", ".md"],
        recursive=False,
        extract_metadata=True
    )
    
    # Should only find files in the root directory, not subdirectories
    assert len(results) == 2
    filenames = [r.filename for r in results]
    assert "sample1.txt" in filenames
    assert "sample2.md" in filenames
    assert not any("sample3.txt" in f for f in filenames)


def test_file_extension_filtering(test_folder, working_dir):
    """Test filtering by file extension."""
    # Initialize indexer
    indexer = GraphRAGIndexer(working_dir=working_dir)
    
    # Run indexing with only .txt files
    results = indexer.index_documents(
        folder_path=test_folder,
        file_extensions=[".txt"],
        recursive=True,
        extract_metadata=True
    )
    
    # Should only find .txt files
    assert len(results) == 2
    filenames = [r.filename for r in results]
    assert "sample1.txt" in filenames
    assert not any("sample2.md" in f for f in filenames)
    assert any("sample3.txt" in f for f in filenames)


def test_metadata_extraction(test_folder, working_dir):
    """Test metadata extraction from files."""
    # Initialize indexer
    indexer = GraphRAGIndexer(working_dir=working_dir)
    
    # Run indexing
    results = indexer.index_documents(
        folder_path=test_folder,
        file_extensions=[".txt", ".md"],
        recursive=True,
        extract_metadata=True
    )
    
    # Verify metadata fields
    for result in results:
        assert result.metadata is not None
        assert result.metadata.filename is not None
        assert result.metadata.file_path is not None
        assert result.metadata.file_size_bytes > 0
        assert result.metadata.file_extension in [".txt", ".md"]
        assert result.metadata.creation_time is not None
        assert result.metadata.modification_time is not None
        assert result.metadata.indexed_time is not None
        assert result.metadata.word_count > 0


def test_invalid_folder():
    """Test handling of invalid folder path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        indexer = GraphRAGIndexer(working_dir=tmpdir)
        non_existent_folder = os.path.join(tmpdir, "non_existent")
        
        # Should return empty results for non-existent folder
        results = indexer.index_documents(folder_path=non_existent_folder)
        assert results == []


def test_empty_folder():
    """Test handling of empty folder."""
    with tempfile.TemporaryDirectory() as tmpdir:
        indexer = GraphRAGIndexer(working_dir=tmpdir)
        empty_folder = os.path.join(tmpdir, "empty")
        os.makedirs(empty_folder, exist_ok=True)
        
        # Should process without errors but return no results for empty folder
        results = indexer.index_documents(folder_path=empty_folder)
        assert len(results) == 0