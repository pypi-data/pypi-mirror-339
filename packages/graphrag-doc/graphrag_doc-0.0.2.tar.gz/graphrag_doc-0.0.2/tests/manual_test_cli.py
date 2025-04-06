"""
Manual test for the GraphRAG CLI functionality.
This test creates sample files in a temporary directory and tests the CLI.
"""
import os
import sys
import json
import tempfile
import shutil
import subprocess
from pathlib import Path

def test_cli():
    """Test the CLI functionality of the GraphRAG indexer."""
    # Create test content
    test_text = """This is a test document.
    It has multiple lines.
    We're using it to test the indexer."""

    # Create temporary directories
    tmp_dir = tempfile.mkdtemp()
    test_folder = os.path.join(tmp_dir, "test_docs")
    working_dir = os.path.join(tmp_dir, "index_dir")
    output_file = os.path.join(tmp_dir, "results.json")
    
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
        
        # Run the CLI command
        cmd = [
            sys.executable, 
            "-m", 
            "graphrag_doc.sdk.cli", 
            "index", 
            test_folder, 
            f"--working-dir={working_dir}", 
            f"--output={output_file}",
            "--file-types=.txt,.md"
        ]
        
        print(f"Executing command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Print results
        print("Command output:")
        print(result.stdout)
        
        if result.stderr:
            print("Command errors:")
            print(result.stderr)
        
        # Check if the output file exists
        if os.path.exists(output_file):
            print(f"Output file created at {output_file}")
            with open(output_file, "r", encoding="utf-8") as f:
                results = json.load(f)
                print(f"Results contain {len(results)} entries")
                for idx, result in enumerate(results):
                    print(f"  {idx+1}. {result['filename']}: {result['status']} - {result['message']}")
        else:
            print(f"Output file not created at {output_file}")
        
        # Check for metadata file
        metadata_path = os.path.join(working_dir, "document_metadata.json")
        if os.path.exists(metadata_path):
            print(f"Metadata file created at {metadata_path}")
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                print(f"Metadata contains {len(metadata)} entries")
        else:
            print(f"Metadata file not created at {metadata_path}")
        
        print("Test completed!")
        
    finally:
        # Clean up
        print(f"Cleaning up temporary directory: {tmp_dir}")
        shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    test_cli()