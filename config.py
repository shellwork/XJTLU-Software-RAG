from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent

# 全局变量
project_name = """
------------------------------------------------

   _____ _           _   _____           _   
  / ____| |         | | |  __ \         | |  
 | |    | |__   __ _| |_| |__) |_ _ _ __| |_ 
 | |    | '_ \ / _` | __|  ___/ _` | '__| __|
 | |____| | | | (_| | |_| |  | (_| | |  | |_ 
  \_____|_| |_|\__,_|\__|_|   \__,_|_|   \__|

------------------------------------------------                                  
"""
welcome = "Welcome to use ChatPart software developed by XJTLU-Software!"
__version__ = "1.0.0"

# 使用 BASE_DIR 构建绝对路径
DATA_PATH = str(BASE_DIR / "data" / "uploads")
CHROMA_PATH = str(BASE_DIR / "chroma")
UPLOAD_DIR = str(BASE_DIR / "data" / "tmp")
CHATICONS = str(BASE_DIR / "frontend_streamlit" / "img" / "icon.png")
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
