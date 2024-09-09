import streamlit as st
from langchain_community.vectorstores import Chroma
from server.model.model_selector import get_model, get_embedding_function

from langchain.prompts import ChatPromptTemplate

from config import CHROMA_PATH, PROMPT_TEMPLATE


def query_chroma(query_text, model_name):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Perform similarity search
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        return None, None

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Use the selected model for generating the response
    model = get_model(model_name)
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    return response_text, sources

# Streamlit 页面设计
st.title("Chroma 数据库查询")

# 输入查询
query_text = st.text_input("请输入查询内容")
model_name = st.selectbox("选择模型", options=["gpt-3.5-turbo", "gpt-4"])

if st.button("执行查询"):
    if query_text:
        response, sources = query_chroma(query_text, model_name)
        if response:
            st.write(f"回答：{response}")
            st.write(f"来源：{', '.join(sources)}")
        else:
            st.write("未找到相关结果或相似度不足")
    else:
        st.error("请输入查询内容")
