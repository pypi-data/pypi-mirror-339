import click
import logging
import json
from graphrag_doc.index.batch_indexer import GraphRAGIndexer

# Configure CLI logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@click.group()
def cli():
    """
    GraphRAG CLI for batch indexing.
    Provides command-line access to batch document processing.
    """
    pass

@click.command()
@click.argument('folder_path')
@click.option('--working-dir', default="graphrag_index", help="Directory for storing indexed data.")
@click.option('--output', default=None, help="Path to save indexing results as a JSON file.")
def index(folder_path: str, working_dir: str, output: str):
    """
    Indexes all text documents in the specified folder.

    Args:
        folder_path (str): Path to the folder containing text documents.
        working_dir (str): Directory where indexed data will be stored.
        output (str): Optional path to save results as a JSON file.

    Returns:
        None
    """
    logging.info(f"Running document indexing for folder: {folder_path}")
    indexer = GraphRAGIndexer(working_dir)
    results = indexer.index_documents(folder_path)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            json.dump([result.model_dump() for result in results], f, indent=4)
        logging.info(f"Results saved to {output}")

cli.add_command(index)

if __name__ == "__main__":
    cli()
