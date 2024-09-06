from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from model.model_selector import get_model, get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
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


# 定义一个生成对话响应的函数
def generate_response(prompt, tools=None, model="default", use_self_model=False, use_local_model=False):
    """
    根据用户的输入和配置，生成对话响应。

    Args:
        prompt (str): 用户的问题。
        tools (list): 选择的工具 (可选)。
        model (str): 要使用的模型名称。
        use_self_model (bool): 是否结合模型直接生成的对话能力。
        use_local_model (bool): 是否使用本地模型推理。

    Returns:
        str: 生成的对话响应或错误提示。
    """

    # 1. 获取嵌入函数，并准备向量数据库
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # 2. 在向量数据库中搜索匹配的文档
    results = db.similarity_search_with_relevance_scores(prompt, k=3)

    # 3. 如果启用了模型对话功能，先获取模型的直接回答
    if use_self_model:
        selected_model = get_model(model, use_local_model=use_local_model)
        model_response = selected_model.invoke(prompt)
        model_answer = model_response.content if hasattr(model_response, 'content') else model_response
    else:
        model_answer = None

    # 4. 如果有RAG结果，生成上下文并进行结合
    if len(results) > 0 and results[0][1] >= 0.7:
        # 有足够相关的RAG结果
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

        # 如果启用了模型对话功能，则合并模型和RAG结果
        if use_self_model:
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            formatted_prompt = prompt_template.format(context=context_text, model_response=model_answer,
                                                      question=prompt)
            final_response = selected_model.invoke(formatted_prompt)
            return final_response.content if hasattr(final_response, 'content') else final_response
        else:
            # 如果没有启用模型对话功能，仅返回RAG结果
            return context_text
    else:
        # 没有RAG结果时的处理
        if use_self_model:
            return model_answer
        else:
            return "无法找到足够相关的结果，请尝试其他问题。"
