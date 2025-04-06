#!/usr/bin/env python3
"""
Sample script to demonstrate how to use the GraphRAG indexer for batch document processing.
"""

import os
import logging
import argparse
import time
from pathlib import Path
from graphrag_doc.index.batch_indexer import GraphRAGIndexer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    """Run batch indexing on a document folder."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Index documents using GraphRAG")
    parser.add_argument("folder_path", help="Path to the folder containing documents")
    parser.add_argument("--working-dir", default="graphrag_index", help="Directory for storing indexed data")
    parser.add_argument("--output", default=None, help="Path to save indexing results as a JSON file")
    parser.add_argument("--file-types", default=".txt,.pdf,.docx,.md", help="Comma-separated list of file extensions to index")
    parser.add_argument("--batch-size", type=int, default=20, help="Number of documents to process in each batch")
    parser.add_argument("--no-recursive", action="store_true", help="Disable recursive search for files")
    parser.add_argument("--no-metadata", action="store_true", help="Disable metadata extraction")

    args = parser.parse_args()

    # Prepare parameters
    folder_path = args.folder_path
    working_dir = args.working_dir
    output = args.output
    extensions = [ext.strip() if ext.strip().startswith('.') else f'.{ext.strip()}' 
                 for ext in args.file_types.split(',')]
    recursive = not args.no_recursive
    extract_metadata = not args.no_metadata

    # Validate folder path
    if not os.path.exists(folder_path):
        logging.error(f"Error: Folder '{folder_path}' does not exist.")
        return 1
    
    # Create working directory if it doesn't exist
    os.makedirs(working_dir, exist_ok=True)
    
    logging.info(f"Starting document indexing process")
    logging.info(f"  - Folder path: {folder_path}")
    logging.info(f"  - Working directory: {working_dir}")
    logging.info(f"  - File types: {', '.join(extensions)}")
    logging.info(f"  - Recursive search: {'Yes' if recursive else 'No'}")
    logging.info(f"  - Extract metadata: {'Yes' if extract_metadata else 'No'}")
    
    # Start timing
    start_time = time.time()
    
    # Initialize indexer
    indexer = GraphRAGIndexer(
        working_dir=working_dir,
        batch_size=args.batch_size
    )
    
    # Run indexing
    results = indexer.index_documents(
        folder_path=folder_path,
        file_extensions=extensions,
        recursive=recursive,
        extract_metadata=extract_metadata
    )
    
    # Report timing
    elapsed_time = time.time() - start_time
    
    # Display summary
    successful = sum(1 for r in results if r.status == "Success")
    failed = len(results) - successful
    logging.info(f"Indexing completed in {elapsed_time:.2f} seconds")
    logging.info(f"Summary: {successful} successful, {failed} failed")
    
    # Save results if output path specified
    if output:
        output_path = Path(output)
        # Create directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump([result.model_dump() for result in results], f, indent=4)
        logging.info(f"Results saved to {output}")
    
    # Print instructions for searching
    logging.info("\nTo query the indexed documents, use:")
    logging.info(f"  from graphrag_doc.sdk.app import query_langgraph")
    logging.info(f"  response = query_langgraph(\"Your query here\")")
    logging.info(f"  print(response[\"response\"])")
    
    return 0

if __name__ == "__main__":
    exit(main())