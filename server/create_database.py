import shutil
import os
from typing import List
from fastapi import UploadFile
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# 导入自定义的加载器
from data_loader.Document_loader import load_documents
from data_loader.JSON_loader import load_json_documents
from data_loader.OCR_document_loader import load_ocr_documents
from model.model_selector import get_embedding_function  # 导入封装的模型选择模块
from pydantic import BaseModel

CHROMA_PATH = "chroma_database"
DATA_PATH = "data/uploads"

class CreateKnowledgeBaseModel(BaseModel):
    kb_name: str
    kb_info: str
    vs_type: str
    embed_model: str

# 初始化上传路径
def initialize_upload_path():
    """初始化文件上传目录"""
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

# 通过检查文件系统获取知识库列表和文件
def get_kb_list():
    """通过文件系统获取知识库列表，即主文件夹下的第一级子文件夹"""
    kb_list = {}
    if os.path.exists(DATA_PATH):
        # 遍历主文件夹下的所有子文件夹
        for kb_name in os.listdir(DATA_PATH):
            kb_path = os.path.join(DATA_PATH, kb_name)
            if os.path.isdir(kb_path):
                # 获取该知识库文件夹（第二级子文件夹）的所有子文件夹，按照文件类别分类
                categories = {}
                for category_name in os.listdir(kb_path):
                    category_path = os.path.join(kb_path, category_name)
                    if os.path.isdir(category_path):
                        # 获取该类别下的所有文件
                        categories[category_name] = os.listdir(category_path)
                kb_list[kb_name] = categories
    return kb_list

def create_kb(kb_info: CreateKnowledgeBaseModel):
    """创建新的知识库（即第一级文件夹）"""
    kb_path = os.path.join(DATA_PATH, kb_info.kb_name)
    if os.path.exists(kb_path):
        return {"status": "error", "message": "知识库已存在"}

    # 创建知识库文件夹
    os.makedirs(kb_path)
    return {"status": "success", "message": f"知识库 {kb_info.kb_name} 创建成功"}

def get_kb_documents(kb_name: str):
    """获取知识库中的文档（即第二级文件夹下的文件）"""
    kb_path = os.path.join(DATA_PATH, kb_name)
    if not os.path.exists(kb_path):
        return {"status": "error", "message": "知识库不存在"}

    categories = {}
    for category_name in os.listdir(kb_path):
        category_path = os.path.join(kb_path, category_name)
        if os.path.isdir(category_path):
            categories[category_name] = os.listdir(category_path)

    return categories

def save_file_to_category(file: UploadFile, kb_name: str):
    """将文件保存到对应知识库的类别文件夹中"""
    file_extension = os.path.splitext(file.filename)[1].lower().strip('.')
    kb_path = os.path.join(DATA_PATH, kb_name, file_extension)

    if not os.path.exists(kb_path):
        os.makedirs(kb_path)

    # 文件保存路径
    file_path = os.path.join(kb_path, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

def delete_kb(kb_name: str):
    """删除指定的知识库（即整个一级文件夹）"""
    kb_path = os.path.join(DATA_PATH, kb_name)
    if os.path.exists(kb_path):
        shutil.rmtree(kb_path)
        return {"status": "success", "message": f"知识库 {kb_name} 已删除"}
    else:
        return {"status": "error", "message": "知识库不存在"}

def delete_kb_files(kb_name: str, files: List[str]):
    """从知识库的类别文件夹中删除指定的文件"""
    kb_path = os.path.join(DATA_PATH, kb_name)
    if not os.path.exists(kb_path):
        return {"status": "error", "message": "知识库不存在"}

    for file_name in files:
        # 假设文件名中包含类别信息（文件夹名）
        file_extension = os.path.splitext(file_name)[1].lower().strip('.')
        file_path = os.path.join(kb_path, file_extension, file_name)

        # 打印要删除的文件路径，帮助调试
        print(f"尝试删除文件: {file_path}")

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"文件 {file_path} 删除成功")
            else:
                print(f"文件 {file_path} 不存在，跳过删除")
        except Exception as e:
            print(f"删除文件 {file_path} 时出错: {e}")
            return {"status": "error", "message": f"删除文件 {file_name} 时发生错误: {str(e)}"}

    return {"status": "success", "message": f"文件已成功从知识库 {kb_name} 中删除"}


# 数据库重建功能
def delete_existing_chroma():
    """删除现有的Chroma数据库目录"""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print(f"Deleted existing database at {CHROMA_PATH}.")

def generate_data_store():
    """生成新的Chroma数据库"""
    ocr_documents = load_ocr_documents()
    non_ocr_documents = load_documents()
    documents = non_ocr_documents + ocr_documents

    chunks = split_text(documents)
    update_chroma(chunks)

    json_documents = load_json_documents(DATA_PATH)
    update_chroma_with_json(json_documents)

def split_text(documents: list[Document]):
    """将文档分块"""
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
    """将文档块更新到Chroma数据库"""
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    db.add_documents(chunks)
    print(f"Added {len(chunks)} chunks to {CHROMA_PATH}.")

def update_chroma_with_json(documents: list[Document]):
    """将JSON文档更新到Chroma数据库"""
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    new_chunks = []
    for document in documents:
        document_id = document.metadata.get("document_id", None)
        document.metadata["hash"] = document_id
        new_chunks.append(document)

    if new_chunks:
        db.add_documents(new_chunks)
        print(f"Added {len(new_chunks)} structured documents to {CHROMA_PATH}.")
    else:
        print("No new structured documents to add.")
