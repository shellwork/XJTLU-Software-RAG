# Special_document_loader.py

from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader

from config import DATA_PATH
from .Picture_Loader import RapidOCRLoader
from .PDFTextLoader import PDFTextLoader  # 导入新的加载器
from langchain.schema import Document
import sys


folder = Path(__file__).resolve().parents[2]
sys.path.append(str(folder))


def load_text_documents(kb_name: str, files: list[str]) -> list[Document]:
    """
    加载通过文本提取的 PDF 文档，基于传入的文件列表只处理指定的文件。

    :param kb_name: 知识库名称。
    :param files: 需要处理的文件列表。
    :return: Document 对象列表。
    """
    base_path = Path(DATA_PATH) / kb_name
    file_set = set(files)  # 将传入的文件列表转换为集合，方便快速查找
    text_documents = []
    # 收集需要处理的 PDF 文件路径
    pdf_paths = [str(pdf_file) for pdf_file in base_path.rglob("*.pdf") if pdf_file.name in file_set]
    if not pdf_paths:
        return text_documents

    # 使用并发加载器处理 PDF 文件
    loader = PDFTextLoader(pdf_paths=pdf_paths)
    text_documents.extend(loader.load())

    return text_documents


def load_ocr_documents(kb_name: str, files: list[str]) -> list[Document]:
    """
    加载 OCR 文档，仅处理图片文件。

    :param kb_name: 知识库名称。
    :param files: 需要处理的文件列表。
    :return: Document 对象列表。
    """
    base_path = Path(kb_name)
    file_set = set(files)  # 将传入的文件列表转换为集合，方便快速查找

    # 加载图片文件并进行 OCR 处理
    image_documents = []
    for img_file in base_path.rglob("*.png"):
        if img_file.name in file_set:  # 仅处理传入文件列表中的文件
            img_loader = DirectoryLoader(str(img_file.parent), loader_cls=RapidOCRLoader, glob=img_file.name)
            image_documents.extend(img_loader.load())

    # 结合 OCR 处理后的图片文档
    documents = image_documents
    return documents


def load_documents_combined(kb_name: str, files: list[str]) -> list[Document]:
    """
    加载所有文档，包括通过文本提取的 PDF 和 OCR 处理的图片。

    :param kb_name: 知识库名称。
    :param files: 需要处理的文件列表。
    :return: Document 对象列表。
    """
    text_docs = load_text_documents(kb_name, files)
    ocr_docs = load_ocr_documents(kb_name, files)
    combined_docs = text_docs + ocr_docs
    return combined_docs
