import shutil
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os

# 导入自定义的加载器
from data_loader.Document_loader import load_documents
from data_loader.JSON_loader import load_json_documents
from data_loader.OCR_document_loader import load_ocr_documents
from model.model_selector import get_embedding_function  # 导入封装的模型选择模块

# Load environment variables. Assumes that project contains .env file with API keys


CHROMA_PATH = "chroma"
DATA_PATH = "../data"

def main():
    # 删除旧的数据库
    delete_existing_chroma()
    # 生成新的数据存储
    generate_data_store()

def delete_existing_chroma():
    # 删除现有的Chroma数据库目录
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print(f"Deleted existing database at {CHROMA_PATH}.")

def generate_data_store():
    # Load OCR documents (PDF, png, jpg)
    ocr_documents = load_ocr_documents()
    # Load non-OCR documents (txt, md, docx, pptx, etc.)
    non_ocr_documents = load_documents()
    documents = non_ocr_documents + ocr_documents

    chunks = split_text(documents)
    update_chroma(chunks)

    # Load and process structured JSON documents
    json_documents = load_json_documents(DATA_PATH)
    update_chroma_with_json(json_documents)

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    return chunks

def update_chroma(chunks: list[Document]):
    # Initialize a new DB.
    embedding_function = get_embedding_function()  # 使用封装的函数获取嵌入模型
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Add all new chunks directly since we're recreating the database
    db.add_documents(chunks)
    print(f"Added {len(chunks)} chunks to {CHROMA_PATH}.")

def update_chroma_with_json(documents: list[Document]):
    # Initialize a new DB.
    embedding_function = get_embedding_function()  # 使用封装的函数获取嵌入模型
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    new_chunks = []
    for document in documents:
        # 使用文件名作为ID
        document_id = document.metadata.get("document_id", None)
        document.metadata["hash"] = document_id  # 将文件名（或文件名的哈希值）作为ID
        new_chunks.append(document)

    if new_chunks:
        db.add_documents(new_chunks)
        print(f"Added {len(new_chunks)} structured documents to {CHROMA_PATH}.")
    else:
        print("No new structured documents to add.")

if __name__ == "__main__":
    main()
