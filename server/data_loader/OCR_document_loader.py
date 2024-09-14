from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader
from .PDF_Loader import RapidOCRPDFLoader
from .Picture_Loader import RapidOCRLoader
from langchain.schema import Document
import sys
folder = Path(__file__).resolve().parents[2]
sys.path.append(str(folder))
from config import DATA_PATH

def load_ocr_documents(kb_name) -> list[Document]:
    base_path = Path(kb_name)

    # Load PDF documents using OCR
    pdf_documents = []
    for pdf_file in base_path.rglob("*.pdf"):
        pdf_loader = DirectoryLoader(pdf_file.parent, loader_cls=RapidOCRPDFLoader, glob=pdf_file.name)
        pdf_documents.extend(pdf_loader.load())

    # Load image documents using OCR
    image_documents = []
    for img_file in base_path.rglob("*.png"):
        img_loader = DirectoryLoader(img_file.parent, loader_cls=RapidOCRLoader, glob=img_file.name)
        image_documents.extend(img_loader.load())

    # Combine OCR-processed documents
    documents = pdf_documents + image_documents
    return documents
