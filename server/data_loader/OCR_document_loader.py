from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader
from .PDF_Loader import RapidOCRPDFLoader
from .Picture_Loader import RapidOCRLoader
from langchain.schema import Document
import sys
folder = Path(__file__).resolve().parents[2]
sys.path.append(str(folder))


def load_ocr_documents(kb_name: str, files: list[str]) -> list[Document]:
    """
    加载 OCR 文档，基于传入的文件列表只处理指定的文件。
    """
    base_path = Path(kb_name)
    file_set = set(files)  # 将传入的文件列表转换为集合，方便快速查找

    # Load PDF documents using OCR
    pdf_documents = []
    for pdf_file in base_path.rglob("*.pdf"):
        if pdf_file.name in file_set:  # 仅处理传入文件列表中的文件
            pdf_loader = DirectoryLoader(str(pdf_file.parent), loader_cls=RapidOCRPDFLoader, glob=pdf_file.name)
            pdf_documents.extend(pdf_loader.load())

    # Load image documents using OCR
    image_documents = []
    for img_file in base_path.rglob("*.png"):
        if img_file.name in file_set:  # 仅处理传入文件列表中的文件
            img_loader = DirectoryLoader(str(img_file.parent), loader_cls=RapidOCRLoader, glob=img_file.name)
            image_documents.extend(img_loader.load())

    # Combine OCR-processed documents
    documents = pdf_documents + image_documents
    return documents
