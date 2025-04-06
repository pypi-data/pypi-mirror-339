import click
import json
import logging
import os
from pathlib import Path
from typing import List, Optional

from graphrag_doc.index.batch_indexer import DocumentIndexResult, GraphRAGIndexer


# Configure CLI logging
logger = logging.getLogger("graphrag_cli")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


@click.group()
def cli():
    """
    GraphRAG CLI for batch indexing.
    Provides command-line access to batch document processing.
    """
    pass


@click.command()
@click.argument('folder_path', type=click.Path(exists=True, file_okay=False, readable=True))
@click.option(
    '--working-dir', 
    default="graphrag_index", 
    help="Directory for storing indexed data."
)
@click.option(
    '--output', 
    default=None, 
    help="Path to save indexing results as a JSON file."
)
@click.option(
    '--file-types', 
    default=".txt,.pdf,.docx,.md", 
    help="Comma-separated list of file extensions to index."
)
@click.option(
    '--batch-size', 
    default=20, 
    type=int, 
    help="Number of documents to process in each batch."
)
@click.option(
    '--recursive/--no-recursive', 
    default=True, 
    help="Whether to recursively search for files in subdirectories."
)
@click.option(
    '--extract-metadata/--no-metadata', 
    default=True, 
    help="Whether to extract metadata from documents."
)
@click.option(
    '--max-workers',
    default=0,
    type=int,
    help="Maximum number of worker threads for parallel processing. Default (0) uses CPU count."
)
def index(
    folder_path: str, 
    working_dir: str, 
    output: Optional[str], 
    file_types: str, 
    batch_size: int, 
    recursive: bool, 
    extract_metadata: bool,
    max_workers: int
):
    """
    Index all supported documents in the specified folder.

    Args:
        folder_path: Path to the folder containing documents.
        working_dir: Directory where indexed data will be stored.
        output: Optional path to save results as a JSON file.
        file_types: Comma-separated list of file extensions to index.
        batch_size: Number of documents to process in each batch.
        recursive: Whether to recursively search for files in subdirectories.
        extract_metadata: Whether to extract metadata from documents.
        max_workers: Maximum number of worker threads for parallel processing.
    """
    logger.info(f"Running document indexing for folder: {folder_path}")
    
    # Parse file types
    extensions = [
        ext.strip() if ext.strip().startswith('.') else f'.{ext.strip()}' 
        for ext in file_types.split(',')
    ]
    
    # Create indexer with specified parameters
    indexer = GraphRAGIndexer(
        working_dir=working_dir,
        batch_size=batch_size
    )
    
    # Run indexing
    results = indexer.index_documents(
        folder_path=folder_path,
        file_extensions=extensions, 
        recursive=recursive,
        extract_metadata=extract_metadata
    )
    
    # Display summary
    successful = sum(1 for r in results if r.status == "Success")
    failed = len(results) - successful
    logger.info(f"Indexing summary: {successful} successful, {failed} failed")
    
    # Save results if output path specified
    if output:
        save_results_to_json(results, output)


def save_results_to_json(results: List[DocumentIndexResult], output_path: str) -> None:
    """
    Save indexing results to a JSON file.
    
    Args:
        results: List of DocumentIndexResult objects
        output_path: Path to save the JSON file
    """
    output_path_obj = Path(output_path)
    
    # Create directory if it doesn't exist
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert results to dictionaries and save
    with open(output_path_obj, "w", encoding="utf-8") as f:
        json_data = [
            result.model_dump() if hasattr(result, 'model_dump') else result.dict()
            for result in results
        ]
        json.dump(json_data, f, indent=4)
        
    logger.info(f"Results saved to {output_path}")


cli.add_command(index)


if __name__ == "__main__":
    cli()