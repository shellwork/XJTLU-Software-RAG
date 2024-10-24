from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent

# 全局变量
project_name = """
------------------------------------------------

   _____ _           _   _____           _       
  / ____| |         | | |  __ \         | |      
 | |    | |__   __ _| |_| |__) |_ _ _ __| |_ ___ 
 | |    | '_ \ / _` | __|  ___/ _` | '__| __/ __|
 | |____| | | | (_| | |_| |  | (_| | |  | |_\__ /
  \_____|_| |_|\__,_|\__|_|   \__,_|_|   \__|___/

------------------------------------------------                                  
"""
welcome = "Welcome to use ChatParts software developed by XJTLU-Software!"
__version__ = "1.0.1"

# 使用 BASE_DIR 构建绝对路径
DATA_PATH = str(BASE_DIR / "data" / "uploads")
CHROMA_PATH = str(BASE_DIR / "chroma")
UPLOAD_DIR = str(BASE_DIR / "data" / "tmp")
CHATICONS = str(BASE_DIR / "frontend_streamlit" / "img" / "icon.png")
# 默认的元数据结构
DEFAULT_METADATA = {
    "chunk_size": 300,
    "chunk_overlap": 100,
    "zh_title_enhance": False,
    "embed_model": "openai",  # 默认的 embedding 模型
    "vs_type": "chroma",  # 默认的向量库类型
    "batches": []  # 用于记录批次处理信息
}
PORT = 6006
LOCAL_MODEL_DIR = "D:\Source Code\PythonProject\XJTLU-Software-RAG\server\model" # 最好用绝对路径
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

RAG_PROMPT_TEMPLATE = """
You are provided with two pieces of information: one from a knowledge base and another from a direct inquiry to a model.
Your task is to analyze and synthesize both pieces of information to produce a comprehensive answer to the question.

Context from the knowledge base:
{context}

---

Response from the model:
{model_response}

---

Based on the above information, provide a comprehensive answer to the following question: {question}
"""
