import fitz
from typing import List

class Document:
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}

def extract_text_from_pdf(pdf_path: str) -> str:
    """从PDF文件中提取文本，忽略图片部分"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_txt(txt_path: str) -> str:
    """从TXT文件中提取文本"""
    with open(txt_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def create_document_from_file(file_path: str) -> List[Document]:
    """根据文件路径提取文本并创建Document对象"""
    if file_path.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.txt'):
        text = extract_text_from_txt(file_path)
    else:
        raise ValueError("不支持的文件类型。只支持 PDF 和 TXT 文件。")

    document = Document(page_content=text, metadata={"source": file_path})
    return [document]

def uploading():
    path = input('Please upload you file: ')
    document = create_document_from_file(path)
    return document


