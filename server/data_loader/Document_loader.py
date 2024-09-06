from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document

DATA_PATH = "data"

def load_documents() -> list[Document]:
    base_path = Path(DATA_PATH)

    # Load .md documents
    md_documents = []
    for md_file in base_path.rglob("*.md"):
        loader = DirectoryLoader(md_file.parent, glob=md_file.name)
        md_documents.extend(loader.load())

    # Load .txt documents
    txt_documents = []
    for txt_file in base_path.rglob("*.txt"):
        txt_loader = DirectoryLoader(txt_file.parent, glob=txt_file.name)
        txt_documents.extend(txt_loader.load())

    # Load .docx documents
    docx_documents = []
    for docx_file in base_path.rglob("*.docx"):
        docx_loader = DirectoryLoader(docx_file.parent, glob=docx_file.name)
        docx_documents.extend(docx_loader.load())

    # Load .pptx documents
    pptx_documents = []
    for pptx_file in base_path.rglob("*.pptx"):
        pptx_loader = DirectoryLoader(pptx_file.parent, glob=pptx_file.name)
        pptx_documents.extend(pptx_loader.load())

    # Combine all non-structured documents
    documents = md_documents + txt_documents + docx_documents + pptx_documents
    return documents
