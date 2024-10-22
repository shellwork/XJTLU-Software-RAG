import logging
from typing import List
from langchain.vectorstores import Chroma

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# 全局变量配置
EXPORT_PATH = "./database_files"  # Chroma数据库导出路径
QUERY = "What was the significance of iGEM 2005?"  # 查询问题
TOP_K = 5  # 返回最相似的文档数量

def query_chroma_db(export_path: str, query: str, top_k: int = 5):
    """根据问题查询Chroma数据库并返回答案和上下文"""
    try:
        # 初始化Chroma数据库
        db = Chroma(persist_directory=export_path)

        # 进行相似性搜索
        results = db.similarity_search(query, k=top_k)

        # 处理和显示结果
        for doc in results:
            if doc.metadata.get("is_qa"):
                # 从page_content中提取问题和上下文
                lines = doc.page_content.split('\n')
                question_line = lines[0] if len(lines) > 0 else ""
                context_line = lines[1] if len(lines) > 1 else ""
                question = question_line.replace('Question: ', '') if question_line.startswith('Question: ') else question_line
                context = context_line.replace('Context: ', '') if context_line.startswith('Context: ') else context_line
                answer = doc.metadata.get("answer", "No answer found")  # 从 metadata 中获取 answer
                url = doc.metadata.get("url", "No URL")
                print(f"Document ID: {doc.metadata.get('document_id')}")
                print(f"Question: {question}")
                print(f"Answer: {answer}")
                print(f"Context: {context}")
                print(f"URL: {url}")
                print("-----")
            else:
                # 对于非问答对的文档，可以选择不显示或显示简要信息
                print(f"Document ID: {doc.metadata.get('document_id')}")
                print(f"Title: {doc.metadata.get('title', 'No Title')}")
                print(f"URL: {doc.metadata.get('url', 'No URL')}")
                print("-----")
    except Exception as e:
        logging.error(f"查询Chroma数据库时出错: {e}", exc_info=True)

def main():
    """主函数，执行查询"""
    try:
        query_chroma_db(EXPORT_PATH, QUERY, TOP_K)
    except Exception as e:
        logging.error(f"主程序出错: {e}", exc_info=True)

if __name__ == "__main__":
    main()
