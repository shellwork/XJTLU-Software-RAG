import os
import json
import logging
from typing import List, Dict
import asyncio
import aiofiles
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from langchain_chroma import Chroma  # 使用 langchain-chroma 包中的 Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings  # 更新为 langchain_huggingface 包中的 HuggingFaceEmbeddings

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# 全局变量配置
DATA_PATH = "./data"  # 数据输入路径
EXPORT_PATH = "./database_files"  # Chroma数据库导出路径
CHUNK_SIZE = 400  # 文本分块大小
CHUNK_OVERLAP = 50  # 文本分块重叠大小
EMBED_MODEL = "/root/autodl-tmp/models/embedding/all-MiniLM-L6-v2"  # 本地模型路径，确保路径正确
CHROMA_PATH = "./database_files"  # Chroma数据库路径

# 默认元数据
DEFAULT_METADATA = {
    "chunk_size": CHUNK_SIZE,
    "chunk_overlap": CHUNK_OVERLAP,
    "embed_model": EMBED_MODEL
}

# 初始化异步线程池
executor = ThreadPoolExecutor(max_workers=8)

async def initialize_paths(data_path: str, export_path: str):
    """初始化数据路径和导出路径"""
    try:
        if not os.path.exists(data_path):
            logging.error(f"数据路径不存在: {data_path}")
            raise FileNotFoundError(f"数据路径不存在: {data_path}")
        else:
            logging.info(f"数据路径已存在: {data_path}")

        if not os.path.exists(export_path):
            os.makedirs(export_path)
            logging.info(f"创建导出路径: {export_path}")
        else:
            logging.info(f"导出路径已存在: {export_path}")

    except Exception as e:
        logging.error(f"初始化路径时出错: {e}", exc_info=True)
        raise

async def load_text_file(file_path: str) -> str:
    """异步加载TXT文件内容"""
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            return await f.read()
    except Exception as e:
        logging.error(f"加载TXT文件 {file_path} 时出错: {e}", exc_info=True)
        return ""

async def load_json_file(file_path: str) -> Dict:
    """异步加载JSON文件内容"""
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            try:
                data = json.loads(content)
                return data
            except json.JSONDecodeError as json_error:
                logging.error(f"JSON解码错误，文件 {file_path} 可能损坏或格式不正确: {json_error}")
                return {}
    except Exception as e:
        logging.error(f"加载JSON文件 {file_path} 时出错: {e}", exc_info=True)
        return {}

async def load_documents(data_path: str) -> List[Document]:
    """加载指定数据路径中的所有支持文档"""
    documents = []
    supported_extensions = ['.txt', '.json', '.pdf']

    logging.info("开始加载文档...")
    for root, _, files in os.walk(data_path):
        load_tasks = []
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            if ext not in supported_extensions:
                logging.warning(f"不支持的文件类型，跳过: {file_path}")
                continue

            if ext == '.txt':
                load_tasks.append(load_text_file(file_path))
            elif ext == '.json':
                load_tasks.append(load_json_file(file_path))
            # PDF文件可以同步读取，PDF的异步读取比较复杂，后续可以考虑优化

        loaded_files = await asyncio.gather(*load_tasks)
        for content, file in zip(loaded_files, files):
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            if ext == '.txt' and content:
                metadata = {"source": file_path, "is_qa": False}
                document = Document(page_content=content, metadata=metadata)
                documents.append(document)
            elif ext == '.json' and isinstance(content, dict):
                # 假设为问答文档
                question = content.get("question", "")
                answer = content.get("answer", "")
                context = content.get("context", "")
                combined_content = f"Question: {question}\nContext: {context}\nAnswer: {answer}"
                metadata = {"source": file_path, "is_qa": True}
                document = Document(page_content=combined_content, metadata=metadata)
                documents.append(document)

    logging.info(f"总共加载了 {len(documents)} 个文档")
    return documents

def split_documents(documents: List[Document], chunk_size: int, chunk_overlap: int) -> List[Document]:
    """根据chunk_size和chunk_overlap将文档分块"""
    try:
        logging.info("开始分块文档...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        logging.info(f"将 {len(documents)} 个文档分块为 {len(chunks)} 个块")
        return chunks
    except Exception as e:
        logging.error(f"分割文档时出错: {e}", exc_info=True)
        return []

def get_embedding_function(embed_model: str) -> HuggingFaceEmbeddings:
    """获取 HuggingFaceEmbeddings 对象"""
    try:
        logging.info(f"加载嵌入模型: {embed_model}")
        embeddings = HuggingFaceEmbeddings(model_name=embed_model)
        return embeddings
    except Exception as e:
        logging.error(f"加载嵌入模型 {embed_model} 时出错: {e}", exc_info=True)
        raise

def embed_documents(chunks: List[Document], embeddings: HuggingFaceEmbeddings) -> List[Document]:
    """将文档块向量化，但不将嵌入向量存储在metadata中"""
    try:
        logging.info("开始向量化文档块...")
        batch_size = 32
        all_chunks = [chunk.page_content for chunk in chunks]
        embeddings_list = embeddings.embed_documents(all_chunks)

        # 移除嵌入向量存储到metadata的代码
        # for i, chunk in enumerate(chunks):
        #     chunk.metadata['embedding'] = embeddings_list[i]

        logging.info(f"已完成向量化 {len(chunks)} 个文档块")
        return chunks
    except Exception as e:
        logging.error(f"向量化文档块时出错: {e}", exc_info=True)
        return []

def update_chroma(chunks: List[Document], embeddings: HuggingFaceEmbeddings, batch_size: int = 40000):
    """将文档块更新到Chroma数据库，分批处理以避免超出最大批量大小"""
    try:
        logging.info("开始更新Chroma数据库...")
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        
        total_chunks = len(chunks)
        for i in range(0, total_chunks, batch_size):
            batch_chunks = chunks[i:i + batch_size]
            db.add_documents(batch_chunks)
            logging.info(f"已添加 {i + len(batch_chunks)} / {total_chunks} 个文档块到 Chroma 数据库")
        
        logging.info(f"已成功添加所有 {total_chunks} 个文档块到 Chroma 数据库")
    except Exception as e:
        logging.error(f"更新Chroma数据库时出错: {e}", exc_info=True)

async def process_data(data_path: str, export_path: str, chunk_size: int, chunk_overlap: int, embed_model: str):
    """处理数据，生成Chroma数据库"""
    try:
        logging.info(f"开始处理数据路径: {data_path}")

        # 加载所有文档
        documents = await load_documents(data_path)
        if not documents:
            logging.warning(f"数据路径 {data_path} 中没有文档需要处理")
            return

        # 分块
        chunks = split_documents(documents, chunk_size, chunk_overlap)
        if not chunks:
            logging.warning("没有生成任何文档块")
            return

        # 获取嵌入对象
        embeddings = get_embedding_function(embed_model)

        # 向量化
        chunks = embed_documents(chunks, embeddings)
        if not chunks:
            logging.warning("没有完成向量化的文档块")
            return

        # 存储到Chroma，分批处理
        update_chroma(chunks, embeddings, batch_size=40000)  # 可根据需要调整 batch_size

        logging.info("数据处理完成")

    except Exception as e:
        logging.error(f"处理数据时出错: {e}", exc_info=True)

async def main():
    """主函数，处理所有数据"""
    try:
        await initialize_paths(DATA_PATH, EXPORT_PATH)
        await process_data(DATA_PATH, EXPORT_PATH, CHUNK_SIZE, CHUNK_OVERLAP, EMBED_MODEL)
    except Exception as e:
        logging.error(f"主程序出错: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())
