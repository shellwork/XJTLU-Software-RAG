from server.document_loaders.pdf_txt_loader import *
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_chunks():
    # document是一个包含单一document对象的list，chunks是包含多个document对象的list
    document = create_document()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50,
        length_function = len,
        is_separator_regex = False,
    )
    chunks = text_splitter.split_documents(document)
    return chunks
