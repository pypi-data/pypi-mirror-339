import os
import logging
from typing import List, Optional
from pydantic import BaseModel, Field
from lightrag import LightRAG
from lightrag.llm.openai import openai_embed, gpt_4o_mini_complete
from PyPDF2 import PdfReader

# Configure logging
logging.basicConfig(
    filename="graphrag_indexer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
logging.getLogger().addHandler(console_handler)

class DocumentIndexResult(BaseModel):
    """Represents the result of an indexed document."""
    filename: str = Field(..., description="Name of the indexed document.")
    status: str = Field(..., description="Status of indexing (Success/Failed).")
    message: str = Field(..., description="Details about the indexing process.")

class GraphRAGIndexer:
    """
    SDK for batch processing documents using LightRAG.

    This class allows users to index multiple text and PDF documents and store embeddings.
    """

    def __init__(self, working_dir: str = "graphrag_index"):
        """
        Initializes the GraphRAG Indexer.
        """
        self.working_dir = working_dir
        self.rag = LightRAG(
            working_dir=working_dir,
            embedding_func=openai_embed,
            llm_model_func=gpt_4o_mini_complete,
            addon_params={
                "insert_batch_size": 20  # Process 20 documents per batch
            }
        )
        logging.info(f"Initialized GraphRAG indexer with working directory: {working_dir}")

    def extract_text_from_pdf(self, pdf_path: str) -> Optional[str]:
        """Extracts text from a PDF file."""
        try:
            reader = PdfReader(pdf_path)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            return text.strip() if text else None
        except Exception as e:
            logging.error(f"Error extracting text from PDF {pdf_path}: {e}", exc_info=True)
            return None

    def index_documents(self, folder_path: str) -> List[DocumentIndexResult]:
        """Indexes all `.txt` and `.pdf` files in the specified folder and subfolders in batches of 20."""
        if not os.path.exists(folder_path):
            logging.error(f"Error: Folder '{folder_path}' does not exist.")
            return []

        indexed_results = []
        logging.info(f"Starting indexing process for folder: {folder_path}")
        
        files_to_index = []
        for root, _, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                if filename.endswith(('.txt', '.pdf')):
                    logging.info(f"Preparing file {filename} for indexing.")
                    content = None
                    try:
                        if filename.endswith('.txt'):
                            with open(file_path, 'r', encoding='utf-8') as file:
                                content = file.read()
                        elif filename.endswith('.pdf'):
                            content = self.extract_text_from_pdf(file_path)
                            if not content:
                                raise ValueError("No extractable text found in PDF")
                        
                        if content:
                            files_to_index.append((filename, content))
                        else:
                            raise ValueError("Content is empty or None")
                    except Exception as e:
                        indexed_results.append(DocumentIndexResult(
                            filename=filename,
                            status="Failed",
                            message=str(e)
                        ))
                        logging.error(f"Error processing file {filename}: {e}", exc_info=True)
        
        # Batch processing
        self.rag.insert(files_to_index)    
        logging.info(f"Indexing completed. Total files processed: {len(indexed_results)}")
        return indexed_results
