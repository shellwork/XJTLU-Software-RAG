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
from config import CHROMA_PATH, DATA_PATH
from response_model import CreateKnowledgeBaseModel

import logging

# 配置日志记录
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# 初始化上传路径
def initialize_upload_path():
    """初始化文件上传目录"""
    try:
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
            logging.info(f"创建数据路径: {DATA_PATH}")
        else:
            logging.info(f"数据路径已存在: {DATA_PATH}")
    except Exception as e:
        logging.error(f"初始化上传路径时出错: {e}", exc_info=True)

# 通过检查文件系统获取知识库列表和文件
def get_kb_list():
    """通过文件系统获取知识库列表，即主文件夹下的第一级子文件夹"""
    kb_list = {}
    try:
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
        logging.debug(f"获取到的知识库列表: {kb_list}")
    except Exception as e:
        logging.error(f"获取知识库列表时出错: {e}", exc_info=True)
    return kb_list

def create_kb(kb_info: CreateKnowledgeBaseModel):
    """创建新的知识库（即第一级文件夹）"""
    try:
        kb_path = os.path.join(DATA_PATH, kb_info.kb_name)
        if os.path.exists(kb_path):
            logging.warning(f"知识库已存在: {kb_info.kb_name}")
            return {"status": "error", "message": "知识库已存在"}

        # 创建知识库文件夹
        os.makedirs(kb_path)
        logging.info(f"知识库创建成功: {kb_info.kb_name}")
        return {"status": "success", "message": f"知识库 {kb_info.kb_name} 创建成功"}
    except Exception as e:
        logging.error(f"创建知识库时出错: {e}", exc_info=True)
        return {"status": "error", "message": f"创建知识库时发生错误: {str(e)}"}

def get_kb_documents(kb_name: str):
    """获取知识库中的文档列表，每个文档包含类别和文件名"""
    try:
        kb_path = os.path.join(DATA_PATH, kb_name)
        if not os.path.exists(kb_path):
            logging.error(f"知识库不存在: {kb_name}")
            return {"status": "error", "message": "知识库不存在"}

        documents = []
        for category_name in os.listdir(kb_path):
            category_path = os.path.join(kb_path, category_name)
            if os.path.isdir(category_path):
                for file_name in os.listdir(category_path):
                    documents.append({
                        "category": category_name,
                        "file_name": file_name
                    })
        logging.debug(f"获取到的文档列表: {documents}")
        return documents
    except Exception as e:
        logging.error(f"获取知识库文档时出错: {e}", exc_info=True)
        return {"status": "error", "message": f"获取知识库文档时发生错误: {str(e)}"}

def save_file_to_category(file: UploadFile, kb_name: str):
    """将文件保存到对应知识库的类别文件夹中"""
    try:
        file_extension = os.path.splitext(file.filename)[1].lower().strip('.')
        kb_path = os.path.join(DATA_PATH, kb_name, file_extension)

        if not os.path.exists(kb_path):
            os.makedirs(kb_path)
            logging.info(f"创建类别文件夹: {kb_path}")

        # 文件保存路径
        file_path = os.path.join(kb_path, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        logging.info(f"文件保存成功: {file_path}")
    except Exception as e:
        logging.error(f"保存文件 {file.filename} 时出错: {e}", exc_info=True)

def delete_kb(kb_name: str):
    """删除指定的知识库（即整个一级文件夹）"""
    try:
        kb_path = os.path.join(DATA_PATH, kb_name)
        if os.path.exists(kb_path):
            shutil.rmtree(kb_path)
            logging.info(f"知识库已删除: {kb_name}")
            return {"status": "success", "message": f"知识库 {kb_name} 已删除"}
        else:
            logging.warning(f"知识库不存在: {kb_name}")
            return {"status": "error", "message": "知识库不存在"}
    except Exception as e:
        logging.error(f"删除知识库 {kb_name} 时出错: {e}", exc_info=True)
        return {"status": "error", "message": f"删除知识库时发生错误: {str(e)}"}

def delete_kb_files(kb_name: str, files: List[dict]):
    """从知识库中删除指定的文件，文件信息包含类别和文件名"""
    try:
        kb_path = os.path.join(DATA_PATH, kb_name)
        logging.debug(f"知识库路径: {kb_path}")

        if not os.path.exists(kb_path):
            logging.error(f"知识库不存在: {kb_name}")
            return {"status": "error", "message": "知识库不存在"}

        for file_info in files:
            category = file_info.get("category")
            file_name = file_info.get("file_name")
            file_path = os.path.join(kb_path, category, file_name)

            logging.debug(f"准备删除文件: {file_path}")

            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    logging.info(f"文件删除成功: {file_path}")
                except PermissionError as pe:
                    logging.error(f"权限错误，无法删除文件 {file_path}: {pe}", exc_info=True)
                    return {"status": "error", "message": f"无法删除文件 {file_name}，权限不足"}
                except Exception as e:
                    logging.error(f"删除文件 {file_path} 时出错: {e}", exc_info=True)
                    return {"status": "error", "message": f"删除文件 {file_name} 时发生错误: {str(e)}"}
            else:
                logging.warning(f"文件不存在，跳过删除: {file_path}")

        return {"status": "success", "message": f"文件已成功从知识库 {kb_name} 中删除"}

    except Exception as e:
        logging.error(f"删除文件时出现错误: {e}", exc_info=True)
        return {"status": "error", "message": f"删除文件时发生错误: {str(e)}"}

# 数据库重建功能
def delete_existing_chroma():
    """删除现有的Chroma数据库目录"""
    try:
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            logging.info(f"已删除现有的Chroma数据库目录: {CHROMA_PATH}")
    except Exception as e:
        logging.error(f"删除Chroma数据库目录时出错: {e}", exc_info=True)

def generate_data_store():
    """生成新的Chroma数据库"""
    try:
        ocr_documents = load_ocr_documents()
        non_ocr_documents = load_documents()
        documents = non_ocr_documents + ocr_documents

        chunks = split_text(documents)
        update_chroma(chunks)

        json_documents = load_json_documents(DATA_PATH)
        update_chroma_with_json(json_documents)
    except Exception as e:
        logging.error(f"生成数据存储时出错: {e}", exc_info=True)

def split_text(documents: list[Document]):
    """将文档分块"""
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        logging.debug(f"将 {len(documents)} 个文档分块为 {len(chunks)} 个块")
        return chunks
    except Exception as e:
        logging.error(f"分割文本时出错: {e}", exc_info=True)
        return []

def update_chroma(chunks: list[Document]):
    """将文档块更新到Chroma数据库"""
    try:
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        db.add_documents(chunks)
        logging.info(f"已添加 {len(chunks)} 个文档块到 Chroma 数据库")
    except Exception as e:
        logging.error(f"更新Chroma数据库时出错: {e}", exc_info=True)

def update_chroma_with_json(documents: list[Document]):
    """将JSON文档更新到Chroma数据库"""
    try:
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        new_chunks = []
        for document in documents:
            document_id = document.metadata.get("document_id", None)
            document.metadata["hash"] = document_id
            new_chunks.append(document)

        if new_chunks:
            db.add_documents(new_chunks)
            logging.info(f"已添加 {len(new_chunks)} 个结构化文档到 Chroma 数据库")
        else:
            logging.warning("没有新的结构化文档需要添加到 Chroma 数据库")
    except Exception as e:
        logging.error(f"更新Chroma数据库（JSON）时出错: {e}", exc_info=True)
