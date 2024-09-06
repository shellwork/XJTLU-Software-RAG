import streamlit as st
import streamlit_antd_components as sac
from streamlit_chatbox import ChatBox
from datetime import datetime
import uuid


# Placeholder for settings
class Settings:
    class model_settings:
        HISTORY_LEN = 5
        TEMPERATURE = 0.7

    class kb_settings:
        DEFAULT_KNOWLEDGE_BASE = "default_kb"
        VECTOR_SEARCH_TOP_K = 5
        SEARCH_ENGINE_TOP_K = 5
        SCORE_THRESHOLD = 0.5
        DEFAULT_SEARCH_ENGINE = "google"

    class tool_settings:
        search_internet = {"search_engine_config": ["google", "bing"]}


# Dummy placeholder for some utility functions
def get_img_base64(image_path):
    return "image_placeholder"


# Dummy placeholder for API request
class ApiRequest:
    # Placeholder for list_knowledge_bases API
    def list_knowledge_bases(self):
        # TODO: Implement the API call to get the list of knowledge bases
        return [{"kb_name": "default_kb"}, {"kb_name": "custom_kb"}]


# Chat box for the UI
chat_box = ChatBox(assistant_avatar=get_img_base64("chat_icon.png"))


# Initializing the session state and widgets
def init_widgets():
    st.session_state.setdefault("history_len", Settings.model_settings.HISTORY_LEN)
    st.session_state.setdefault("selected_kb", Settings.kb_settings.DEFAULT_KNOWLEDGE_BASE)
    st.session_state.setdefault("kb_top_k", Settings.kb_settings.VECTOR_SEARCH_TOP_K)
    st.session_state.setdefault("se_top_k", Settings.kb_settings.SEARCH_ENGINE_TOP_K)
    st.session_state.setdefault("score_threshold", Settings.kb_settings.SCORE_THRESHOLD)
    st.session_state.setdefault("search_engine", Settings.kb_settings.DEFAULT_SEARCH_ENGINE)
    st.session_state.setdefault("return_direct", False)
    st.session_state.setdefault("cur_conv_name", chat_box.cur_chat_name)
    st.session_state.setdefault("last_conv_name", chat_box.cur_chat_name)
    st.session_state.setdefault("file_chat_id", None)


def kb_chat(api=None):
    # Initialize widgets
    init_widgets()

    with st.sidebar:
        st.title("RAG 对话系统")

        tabs = st.tabs(["RAG 配置", "会话设置"])

        # RAG 配置
        with tabs[0]:
            dialogue_modes = ["知识库问答", "文件对话", "搜索引擎问答"]
            dialogue_mode = st.selectbox("选择对话模式", dialogue_modes, key="dialogue_mode")

            st.divider()
            st.number_input("历史对话轮数", 0, 20, key="history_len")
            st.number_input("匹配知识条数", 1, 20, key="kb_top_k")
            st.slider("知识匹配分数阈值", 0.0, 2.0, step=0.01, key="score_threshold")
            st.checkbox("仅返回检索结果", key="return_direct")

            # 知识库选择
            if dialogue_mode == "知识库问答":
                # TODO: Implement the API call to list knowledge bases
                kb_list = [x["kb_name"] for x in api.list_knowledge_bases()] if api else []
                st.selectbox("选择知识库", kb_list, key="selected_kb")

            # 文件对话模式
            elif dialogue_mode == "文件对话":
                st.file_uploader("上传文件", accept_multiple_files=True)

            # 搜索引擎模式
            elif dialogue_mode == "搜索引擎问答":
                search_engine_list = list(Settings.tool_settings.search_internet["search_engine_config"])
                st.selectbox("选择搜索引擎", search_engine_list, key="search_engine")

        # 会话设置
        with tabs[1]:
            conv_names = chat_box.get_chat_names()
            st.selectbox("选择会话", conv_names, key="cur_conv_name")

    # 显示聊天记录
    chat_box.output_messages()

    # 底部的输入框
    prompt = st.chat_input("请输入对话内容，换行请使用Shift+Enter")
    if prompt:
        chat_box.user_say(prompt)
        chat_box.ai_say(f"回复: {prompt}")

    now = datetime.now()
    st.download_button(
        "导出记录",
        "".join(chat_box.export2md()),
        file_name=f"{now:%Y-%m-%d %H.%M}_对话记录.md",
        mime="text/markdown",
    )


# 主函数入口
if __name__ == "__main__":
    # Placeholder for api instantiation
    api = ApiRequest()
    kb_chat(api=api)
