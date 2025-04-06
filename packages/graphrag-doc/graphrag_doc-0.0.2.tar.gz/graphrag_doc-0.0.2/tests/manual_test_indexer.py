"""
Manual test for the GraphRAG indexer functionality.
This test creates sample files in a temporary directory and tests the indexer.
"""
import os
import json
import tempfile
import shutil
from pathlib import Path
from graphrag_doc.index.batch_indexer import GraphRAGIndexer

def test_indexer():
    """Test the basic functionality of the indexer."""
    # Create test content
    test_text = """This is a test document.
    It has multiple lines.
    We're using it to test the indexer."""

    # Create temporary directories
    tmp_dir = tempfile.mkdtemp()
    test_folder = os.path.join(tmp_dir, "test_docs")
    working_dir = os.path.join(tmp_dir, "index_dir")
    
    try:
        # Create test folder structure
        os.makedirs(test_folder, exist_ok=True)
        os.makedirs(working_dir, exist_ok=True)
        
        # Create a text file
        with open(os.path.join(test_folder, "sample1.txt"), "w", encoding="utf-8") as f:
            f.write(test_text)
        
        # Create a markdown file
        with open(os.path.join(test_folder, "sample2.md"), "w", encoding="utf-8") as f:
            f.write("# Test Markdown\n\n" + test_text)
        
        # Create a subdirectory
        subdir = os.path.join(test_folder, "subdir")
        os.makedirs(subdir, exist_ok=True)
        
        # Create another text file in the subdirectory
        with open(os.path.join(subdir, "sample3.txt"), "w", encoding="utf-8") as f:
            f.write("This is a document in a subdirectory.\n" + test_text)
        
        print(f"Created test files in {test_folder}")
        
        # Initialize indexer
        indexer = GraphRAGIndexer(working_dir=working_dir)
        print("Initialized indexer")
        
        # Run indexing
        results = indexer.index_documents(
            folder_path=test_folder,
            file_extensions=[".txt", ".md"],
            recursive=True,
            extract_metadata=True
        )
        
        # Print results
        print(f"Indexed {len(results)} documents:")
        for result in results:
            print(f"  - {result.filename}: {result.status} - {result.message}")
            if result.metadata:
                print(f"    Size: {result.metadata.file_size_bytes} bytes")
                print(f"    Words: {result.metadata.word_count}")
        
        # Check for metadata file
        metadata_path = os.path.join(working_dir, "document_metadata.json")
        if os.path.exists(metadata_path):
            print(f"Metadata file created at {metadata_path}")
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                print(f"Metadata contains {len(metadata)} entries")
        
        print("Test completed successfully!")
        
    finally:
        # Clean up
        print(f"Cleaning up temporary directory: {tmp_dir}")
        shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    test_indexer()