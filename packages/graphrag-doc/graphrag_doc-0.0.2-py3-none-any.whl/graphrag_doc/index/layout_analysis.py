import os
import base64
import logging
import fitz  # PyMuPDF for PDFs
from pdfminer.high_level import extract_text
from PIL import Image
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional

# Initialize OpenAI client
client = OpenAI()

# Define supported file extensions
SUPPORTED_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
SUPPORTED_PDF_EXTENSION = ".pdf"

# Setup Logging
log_file = "layout_analysis.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),  # Save logs to file
        logging.StreamHandler()         # Print logs to console
    ]
)
logger = logging.getLogger(__name__)


class OCRResult(BaseModel):
    """Pydantic model for OCR results."""
    filename: str = Field(..., description="Name of the processed file.")
    content: str = Field(..., description="Extracted text content from the file.")


class PDFProcessingResult(BaseModel):
    """Pydantic model for PDF processing results."""
    filename: str = Field(..., description="Name of the processed PDF file.")
    text_content: Optional[str] = Field(None, description="Extracted text if PDF is text-based.")
    images_ocr_results: List[OCRResult] = Field(default_factory=list, description="OCR results from images in the PDF.")


def encode_image(image_path: str) -> str:
    """Convert an image file to a Base64-encoded string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def is_pdf_text_based(pdf_path: str) -> bool:
    """Check if a PDF is text-based or image-based."""
    logger.info(f"Checking if PDF is text-based: {pdf_path}")
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text("text")  # type: ignore
        if text.strip():
            # Found text in at least one page, so this PDF is text-based
            return True
    return False


def extract_images_from_pdf(pdf_path: str) -> List[bytes]:
    """Extract images from a PDF file."""
    logger.info(f"Extracting images from PDF: {pdf_path}")
    images = []
    doc = fitz.open(pdf_path)
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(image_bytes)
    return images


def ocr_image(image_path: str) -> OCRResult:
    """Perform OCR on an image using OpenAI Vision API."""
    logger.info(f"Performing OCR on image: {image_path}")
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Extract all text from this image while preserving layout. "
                            "Maintain structure, including headings, lists, and tables. "
                            "Output format as Markdown, and only contain content from the image file."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )

    extracted_text = response.choices[0].message.content if response.choices[0].message.content else ""
    extracted_text = extracted_text.strip()

    logger.info(f"OCR completed for {image_path}, extracted {len(extracted_text)} characters.")
    return OCRResult(filename=os.path.basename(image_path), content=extracted_text)


def get_text_save_path(original_path: str, file_root: str, save_root: str) -> str:
    """
    Compute the corresponding .txt file path in the `save_root` directory
    that mirrors the structure of `file_root`.
    """
    relative_path = os.path.relpath(original_path, file_root)
    save_path = os.path.join(save_root, os.path.splitext(relative_path)[0] + ".txt")
    return save_path


def save_text(save_path: str, content: str):
    """Save extracted text to a .txt file (creates directories as needed)."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(content)
    logger.info(f"Saved extracted text to: {save_path}")


def process_pdf(pdf_path: str, file_root: str, save_root: str) -> PDFProcessingResult:
    """Process a PDF file and extract text while maintaining layout."""
    logger.info(f"Processing PDF: {pdf_path}")
    filename = os.path.basename(pdf_path)

    # If PDF is text-based, extract directly
    if is_pdf_text_based(pdf_path):
        text_content = extract_text(pdf_path)
        save_path = get_text_save_path(pdf_path, file_root, save_root)
        save_text(save_path, text_content)
        return PDFProcessingResult(filename=filename, text_content=text_content, images_ocr_results=[])

    # Otherwise, it's image-based; extract images and perform OCR
    extracted_images = extract_images_from_pdf(pdf_path)
    ocr_results = []
    combined_text = ""

    for index, image_bytes in enumerate(extracted_images):
        temp_image_path = f"temp_image_{index}.png"
        with open(temp_image_path, "wb") as img_file:
            img_file.write(image_bytes)

        ocr_result = ocr_image(temp_image_path)
        ocr_results.append(ocr_result)

        # Append only the extracted text; no headings or labels
        combined_text += ocr_result.content + "\n"

        # Cleanup temporary image
        os.remove(temp_image_path)

    # Save combined text from all images
    save_path = get_text_save_path(pdf_path, file_root, save_root)
    save_text(save_path, combined_text)

    return PDFProcessingResult(filename=filename, text_content=None, images_ocr_results=ocr_results)


def process_image(image_path: str, file_root: str, save_root: str) -> OCRResult:
    """Process an image file with OCR and save the extracted text."""
    logger.info(f"Processing Image: {image_path}")
    ocr_result = ocr_image(image_path)

    # Save extracted text
    save_path = get_text_save_path(image_path, file_root, save_root)
    save_text(save_path, ocr_result.content)

    return ocr_result


def process_files_recursively(file_root: str, save_root: str):
    """
    Recursively process all PDFs and images in a directory, extracting text and saving it.
    Skips any file that has already been processed (i.e., .txt output already exists).
    """
    logger.info(f"Starting processing in directory: {file_root}")

    for root, _, files in os.walk(file_root):
        for file in files:
            file_path = os.path.join(root, file)

            # Determine the would-be .txt save path
            txt_save_path = get_text_save_path(file_path, file_root, save_root)

            # Skip if a .txt file already exists for this file
            if os.path.exists(txt_save_path):
                logger.info(f"Skipping already processed file: {file_path}")
                continue

            if file.lower().endswith(SUPPORTED_PDF_EXTENSION):
                logger.info(f"Processing PDF: {file_path}")
                process_pdf(file_path, file_root, save_root)

            elif file.lower().endswith(SUPPORTED_IMAGE_EXTENSIONS):
                logger.info(f"Processing Image: {file_path}")
                process_image(file_path, file_root, save_root)

    logger.info("Processing completed! Extracted text saved in the specified save_root directory.")


if __name__ == "__main__":
    file_root = input("Enter the root directory path of files: ")
    save_root = input("Enter the save directory path: ")
    process_files_recursively(file_root, save_root)
