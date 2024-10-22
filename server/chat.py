from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from model.model_selector import get_model, get_embedding_function
from pathlib import Path
import sys

folder = Path(__file__).resolve().parents[1]
sys.path.append(str(folder))
from config import RAG_PROMPT_TEMPLATE, CHROMA_PATH


def generate_response(prompt, eb_models, provider, tools=None, model="gpt-3.5-turbo", use_self_model=False,
                      use_local_model=False):
    """
    根据用户的输入和配置，生成对话响应。

    Args:
        provider: 指定特定的模型提供商
        eb_models: 要使用的embedding模型名称
        prompt (str): 用户的问题。
        tools (list): 选择的工具 (可选)。
        model (str): 要使用的模型名称。
        use_self_model (bool): 是否结合模型直接生成的对话能力。
        use_local_model (bool): 是否使用本地模型推理。

    Returns:
        dict: 包含响应内容及相关信息。
    """

    # 1. 获取嵌入函数，并准备向量数据库
    embedding_function = get_embedding_function(eb_models, provider, use_local_model)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # 2. 在向量数据库中搜索匹配的文档
    results = db.similarity_search_with_relevance_scores(prompt, k=3)

    # 准备返回结构
    response = {}

    if not use_self_model:
        # 检索模式，仅返回相关文档块和引用
        if len(results) > 0 and results[0][1] >= 0.7:
            chunks = [doc.page_content for doc, _score in results]
            references = [doc.metadata.get('source', 'Unknown') for doc, _score in results]

            response['chunks'] = chunks
            response['references'] = references
        else:
            response['chunks'] = []
            response['references'] = []
    else:
        # 对话模式，结合模型生成回答
        selected_model = get_model(model, provider, local=use_local_model)  # 直接指定了默认模型提供商为provider
        model_response = selected_model.invoke(prompt)
        model_answer = model_response.content if hasattr(model_response, 'content') else model_response

        if len(results) > 0 and results[0][1] >= 0.7:
            # 有足够相关的RAG结果
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            references = [doc.metadata.get('source', 'Unknown') for doc, _score in results]

            prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
            formatted_prompt = prompt_template.format(context=context_text, model_response=model_answer,
                                                      question=prompt)
            final_response = selected_model.invoke(formatted_prompt)
            combined_answer = final_response.content if hasattr(final_response, 'content') else final_response

            response['answer'] = combined_answer
            response['references'] = references
        else:
            # 没有RAG结果，直接返回模型回答
            response['answer'] = model_answer
            response['references'] = []

    return response
