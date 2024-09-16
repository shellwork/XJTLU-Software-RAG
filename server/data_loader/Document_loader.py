from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document
import sys
folder = Path(__file__).resolve().parents[2]
sys.path.append(str(folder))


def load_documents(kb_name: str, files: list[str]) -> list[Document]:
    """
    加载普通文档，基于传入的文件列表只处理指定的文件。
    """
    base_path = Path(kb_name)
    file_set = set(files)  # 将传入的文件列表转换为集合，方便快速查找

    # Load .md documents
    md_documents = []
    for md_file in base_path.rglob("*.md"):
        if md_file.name in file_set:  # 仅处理传入文件列表中的文件
            loader = DirectoryLoader(str(md_file.parent), glob=md_file.name)
            md_documents.extend(loader.load())

    # Load .txt documents
    txt_documents = []
    for txt_file in base_path.rglob("*.txt"):
        if txt_file.name in file_set:  # 仅处理传入文件列表中的文件
            txt_loader = DirectoryLoader(str(txt_file.parent), glob=txt_file.name)
            txt_documents.extend(txt_loader.load())

    # Load .docx documents
    docx_documents = []
    for docx_file in base_path.rglob("*.docx"):
        if docx_file.name in file_set:  # 仅处理传入文件列表中的文件
            docx_loader = DirectoryLoader(str(docx_file.parent), glob=docx_file.name)
            docx_documents.extend(docx_loader.load())

    # Load .pptx documents
    pptx_documents = []
    for pptx_file in base_path.rglob("*.pptx"):
        if pptx_file.name in file_set:  # 仅处理传入文件列表中的文件
            pptx_loader = DirectoryLoader(str(pptx_file.parent), glob=pptx_file.name)
            pptx_documents.extend(pptx_loader.load())

    # Combine all non-structured documents
    documents = md_documents + txt_documents + docx_documents + pptx_documents
    return documents
