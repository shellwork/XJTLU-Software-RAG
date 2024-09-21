import json
import shutil
import os
from typing import List
from fastapi import UploadFile
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# 导入自定义的加载器
from data_loader.Document_loader import load_ori_documents
from data_loader.JSON_loader import load_json_documents
from data_loader.Special_document_loader import load_ocr_documents, load_documents_combined
from model.model_selector import get_embedding_function  # 导入封装的模型选择模块
from config import CHROMA_PATH, DATA_PATH, DEFAULT_METADATA

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


# 初始化参数存储列表
def initialize_metadata(kb_name: str):
    """
    检查并初始化指定知识库的 metadata.json 文件，如果不存在则创建并写入默认值。
    """
    kb_path = Path(kb_name)
    metadata_path = kb_path / "metadata.json"

    # 如果 metadata.json 不存在，则创建并初始化
    if not metadata_path.exists():
        try:
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_METADATA, f, ensure_ascii=False, indent=4)
            logging.info(f"初始化 {kb_name} 的 metadata.json 文件")
        except Exception as e:
            logging.error(f"初始化 metadata.json 文件时出错: {e}")
    else:
        logging.info(f"{kb_name} 的 metadata.json 已存在，无需初始化")


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


def create_kb(kb_name: str, kb_info: str, vs_type: str, embed_model: str):
    """创建新的知识库，并根据提供的 embed_model 进行配置"""
    try:
        kb_path = os.path.join(DATA_PATH, kb_name)
        if os.path.exists(kb_path):
            logging.warning(f"知识库已存在: {kb_name}")
            return {"status": "error", "message": "知识库已存在"}

        # 创建知识库文件夹
        os.makedirs(kb_path)
        logging.info(f"知识库创建成功: {kb_name}")
        # 检查并初始化 metadata.json
        initialize_metadata(kb_name)
        # 将知识库信息存储到 metadata.json 中，包括 embed_model 和 vs_type
        metadata = {
            "kb_name": kb_name,
            "kb_info": kb_info,
            "vs_type": vs_type,
            "embed_model": embed_model,  # 将 embed_model 记录下来
            "chunk_size": 300,
            "chunk_overlap": 100,
            "zh_title_enhance": False
        }
        update_kb_metadata(kb_name, metadata)  # 记录元数据

        return {"status": "success", "message": f"知识库 {kb_name} 创建成功"}

    except Exception as e:
        logging.error(f"创建知识库时出错: {e}", exc_info=True)
        return {"status": "error", "message": f"创建知识库时发生错误: {str(e)}"}


def get_kb_documents(kb_name: str):
    """获取知识库中的文档列表，每个文档包含类别、文件名、文件大小、chunk_size 和 chunk_overlap"""
    try:
        kb_path = os.path.join(DATA_PATH, kb_name)
        if not os.path.exists(kb_path):
            logging.error(f"知识库不存在: {kb_name}")
            return {"status": "error", "message": "知识库不存在"}

        # 读取 metadata 信息
        metadata = read_kb_metadata(kb_name)
        batches = metadata.get("batches", [])
        global_chunk_size = metadata.get("chunk_size", 300)  # 全局默认 chunk_size
        global_chunk_overlap = metadata.get("chunk_overlap", 100)  # 全局默认 chunk_overlap

        # 获取文件列表
        documents = []
        for category_name in os.listdir(kb_path):
            category_path = os.path.join(kb_path, category_name)
            if os.path.isdir(category_path):
                for file_name in os.listdir(category_path):
                    file_path = os.path.join(category_path, file_name)

                    # 获取文件大小
                    file_size = os.path.getsize(file_path)

                    # 查找该文件的分块信息
                    file_chunk_size = global_chunk_size
                    file_chunk_overlap = global_chunk_overlap
                    for batch in batches:
                        if file_name in batch["files"]:
                            file_chunk_size = batch.get("chunk_size", global_chunk_size)
                            file_chunk_overlap = batch.get("chunk_overlap", global_chunk_overlap)
                            break

                    # 如果没有找到匹配的批次，继续使用全局默认的 chunk_size 和 chunk_overlap

                    documents.append({
                        "category": category_name,
                        "file_name": file_name,
                        "file_size": file_size,
                        "chunk_size": file_chunk_size,
                        "chunk_overlap": file_chunk_overlap
                    })

        logging.debug(f"获取到的文档列表: {documents}")
        return documents

    except Exception as e:
        logging.error(f"获取知识库文档时出错: {e}", exc_info=True)
        return {"status": "error", "message": f"获取知识库文档时发生错误: {str(e)}"}


def save_file_to_category(file: UploadFile, kb_name: str) -> str:
    """将文件保存到对应知识库的类别文件夹中，并返回文件名"""
    try:
        # 获取文件扩展名，作为类别文件夹
        file_extension = os.path.splitext(file.filename)[1].lower().strip('.')
        kb_path = os.path.join(DATA_PATH, kb_name, file_extension)

        # 如果类别文件夹不存在，则创建
        if not os.path.exists(kb_path):
            os.makedirs(kb_path)
            logging.info(f"创建类别文件夹: {kb_path}")

        # 生成文件保存路径
        file_path = os.path.join(kb_path, file.filename)

        # 保存文件
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        logging.info(f"文件保存成功: {file_path}")

        # 返回文件名
        return file.filename

    except Exception as e:
        logging.error(f"保存文件 {file.filename} 时出错: {e}", exc_info=True)
        return "error_name"

def delete_files_from_metadata(kb_name, files_to_delete):
    """从 metadata 中删除对应的文件"""
    metadata = read_kb_metadata(kb_name)

    for batch in metadata.get("batches", []):
        batch["files"] = [f for f in batch.get("files", []) if f not in files_to_delete]

    # 删除所有文件为空的批次
    metadata["batches"] = [batch for batch in metadata["batches"] if batch["files"]]

    # 更新 metadata.json
    update_kb_metadata(kb_name, metadata)

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
                    delete_files_from_metadata(kb_name, file_name)
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


# 数据库删除功能
def delete_existing_chroma():
    """删除现有的Chroma数据库目录"""
    try:
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            logging.info(f"已删除现有的Chroma数据库目录: {CHROMA_PATH}")
    except Exception as e:
        logging.error(f"删除Chroma数据库目录时出错: {e}", exc_info=True)


def process_batches(kb_name: str):
    """
    遍历知识库中的所有批次，分别调用 generate_data_store 进行处理。
    如果有文件没有分配到批次中，则将其分配到默认批次，并给予默认参数。
    """
    try:
        # 读取知识库的元数据，包括批次信息
        metadata = read_kb_metadata(kb_name)
        kb_path = Path(kb_name)

        # 检查是否存在批次信息
        if "batches" not in metadata:
            metadata["batches"] = []

        # 获取批次中已分配的文件总数
        batch_files = set(file for batch in metadata["batches"] for file in batch.get("files", []))
        total_batch_files_count = len(batch_files)

        # 获取实际知识库目录中的文件总数
        all_files = {str(file) for file in kb_path.rglob("*") if file.is_file()}
        total_actual_files_count = len(all_files)

        # 如果批次文件数目等于实际文件数目，则跳过目录遍历
        if total_actual_files_count == total_batch_files_count:
            logging.info(f"批次文件数目与实际文件数目相同，跳过未分配文件的检查")
        else:
            # 找到未被分配到任何批次的文件
            unbatched_files = all_files - batch_files
            if unbatched_files:
                logging.info(f"发现 {len(unbatched_files)} 个未分配到批次的文件，将分配到默认批次")

                # 创建一个默认批次并分配未分配的文件
                default_batch = {
                    "batch_id": f"default_batch_{len(metadata['batches']) + 1}",
                    "chunk_size": metadata.get("chunk_size", 300),
                    "chunk_overlap": metadata.get("chunk_overlap", 100),
                    "zh_title_enhance": metadata.get("zh_title_enhance", False),
                    "files": list(unbatched_files)
                }

                # 添加默认批次到元数据中
                metadata["batches"].append(default_batch)
                update_kb_metadata(kb_name, {"batches": metadata["batches"]})
                logging.info(f"已创建默认批次并更新元数据：{default_batch['batch_id']}")

        # 遍历每个批次进行处理
        for batch in metadata["batches"]:
            logging.info(f"处理批次 {batch['batch_id']}，文件数量：{len(batch['files'])}")

            # 获取每批次的处理参数
            chunk_size = batch.get("chunk_size", metadata["chunk_size"])  # 批次优先，默认全局
            chunk_overlap = batch.get("chunk_overlap", metadata["chunk_overlap"])  # 批次优先，默认全局
            zh_title_enhance = batch.get("zh_title_enhance", metadata["zh_title_enhance"])  # 批次优先，默认全局
            embed_model = metadata.get("embed_model", "openai")  # 全局设置
            vs_type = metadata.get("vs_type", "chroma")  # 全局设置
            files = batch.get("files", [])  # 获取该批次的文件列表
            if not files:
                logging.warning(f"批次 {batch['batch_id']} 中没有文件")
                continue

            # 调用 generate_data_store 处理当前批次
            generate_data_store(
                kb_name=kb_name,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                zh_title_enhance=zh_title_enhance,
                embed_model=embed_model,
                vs_type=vs_type,
                files=files  # 传递批次中的文件列表
            )

        logging.info(f"知识库 {kb_name} 的所有批次已处理完毕")
        return {"status": "success", "message": f"所有批次已处理完毕"}

    except Exception as e:
        logging.error(f"处理批次时出错: {e}", exc_info=True)
        return {"status": "error", "message": f"处理批次时出错: {str(e)}"}


def generate_data_store(kb_name: str, chunk_size: int, chunk_overlap: int, zh_title_enhance: bool, embed_model: str, vs_type: str, files: list):
    """
    处理指定文件的批次，包括分块、向量化以及其他必要的步骤。
    支持 OCR 文档、普通文档的分块和向量化，JSON 文档直接更新。
    """
    try:
        kb_path = os.path.join(DATA_PATH, kb_name)

        # 根据传入的文件名列表加载 OCR 文档和普通文档

        ocr_documents = load_ocr_documents(kb_path, files)
        print(f"pdf_text")
        pdf_text = load_documents_combined(kb_name, files)
        non_ocr_documents = load_ori_documents(kb_path, files)
        all_documents = non_ocr_documents + ocr_documents + pdf_text

        if all_documents:
            # 根据 chunk_size 和 chunk_overlap 进行分块
            document_chunks = split_text(all_documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            logging.info(f"文档已分块，生成了 {len(document_chunks)} 个块")

            # 处理 zh_title_enhance 参数，如果启用了该功能，进行特殊的处理
            if zh_title_enhance:
                # 在这里添加任何与 zh_title_enhance 相关的处理逻辑
                logging.debug(f"启用了中文标题增强功能，处理中文标题")

            # 向量化处理并更新数据库
            if vs_type == "chroma":
                update_chroma(document_chunks, embed_model=embed_model)
            # 可以加入其他数据库

        # 根据传入的文件名列表加载并处理 JSON 文档（不进行分块）
        json_documents = load_json_documents(kb_path, files)
        if json_documents:
            logging.info(f"JSON文档已加载，开始处理 {len(json_documents)} 个文档")
            if vs_type == "chroma":
                update_chroma_with_json(json_documents, embed_model=embed_model)
            # 可以加入其他数据库
        else:
            logging.info("没有新的 JSON 文档需要处理")

    except Exception as e:
        logging.error(f"处理和生成数据存储时出错: {e}", exc_info=True)


def read_kb_metadata(kb_name: str) -> dict:
    """
    读取指定知识库的元数据文件 (metadata.json)，返回包含全局和批次信息的字典。
    如果文件不存在，则调用初始化函数创建文件并读取。
    """
    metadata_path = os.path.join(DATA_PATH, kb_name, "metadata.json")

    # 检查 metadata 文件是否存在，如果不存在则调用初始化函数
    if not os.path.exists(metadata_path):
        logging.warning(f"知识库 {kb_name} 的元数据文件不存在，正在初始化...")
        initialize_metadata(kb_name)  # 调用初始化函数创建元数据文件

    # 尝试读取元数据文件
    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            logging.info(f"从 metadata.json 中读取到的参数：{metadata}")
            return metadata
    except Exception as e:
        logging.error(f"读取元数据文件时出错: {e}")
        raise RuntimeError(f"读取知识库 {kb_name} 的元数据文件失败")


def split_text(documents: list[Document], chunk_size: int, chunk_overlap: int):
    """根据给定的 chunk_size 和 chunk_overlap 将文档分块"""
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        logging.debug(f"将 {len(documents)} 个文档分块为 {len(chunks)} 个块")
        return chunks
    except Exception as e:
        logging.error(f"分割文本时出错: {e}", exc_info=True)
        return []


def update_chroma(chunks: list[Document], embed_model: str):
    """将文档块更新到Chroma数据库"""
    try:
        embedding_function = get_embedding_function(embed_model)
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        db.add_documents(chunks)
        logging.info(f"已添加 {len(chunks)} 个文档块到 Chroma 数据库")
    except Exception as e:
        logging.error(f"更新Chroma数据库时出错: {e}", exc_info=True)


def update_chroma_with_json(documents: list[Document], embed_model: str):
    """将JSON文档更新到Chroma数据库"""
    try:
        embedding_function = get_embedding_function(embed_model)
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


def update_kb_metadata(kb_name: str, metadata: dict, is_batch: bool = False):
    """
    更新知识库的元数据，将配置信息（如 chunk_size、chunk_overlap 等）存储到 JSON 文件中。
    如果 is_batch 为 True，则将该元数据作为一个新的批次添加到 batches 列表中；
    否则，更新全局元数据。
    """
    try:
        # 定义知识库元数据文件的路径
        metadata_path = os.path.join(DATA_PATH, kb_name, "metadata.json")

        # 如果元数据文件存在，读取现有的内容
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                existing_metadata = json.load(f)
        else:
            existing_metadata = {"batches": []}  # 初始化批次列表

        if is_batch:
            # 更新元数据，将新的批次信息添加到 batches 列表
            if "batches" not in existing_metadata:
                existing_metadata["batches"] = []
            existing_metadata["batches"].append(metadata)
        else:
            # 更新全局元数据
            existing_metadata.update(metadata)

        # 将更新后的元数据写回文件
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(existing_metadata, f, ensure_ascii=False, indent=4)

        logging.info(f"已成功更新知识库 {kb_name} 的元数据")

    except Exception as e:
        logging.error(f"更新知识库 {kb_name} 的元数据时出错: {e}", exc_info=True)
