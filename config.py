# 全局变量

__version__ = "1.0.0"

DATA_PATH = "data/uploads"
CHROMA_PATH = "chroma"
UPLOAD_DIR = "data/tmp"
CHATICONS = "frontend_streamlit/img/icon.png"
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