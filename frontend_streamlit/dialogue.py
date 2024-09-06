import streamlit as st
import streamlit_antd_components as sac
from streamlit_chatbox import ChatBox
import uuid
from datetime import datetime
from streamlit_extras.bottom_container import bottom

# 初始化ChatBox
chat_box = ChatBox(assistant_avatar="path_to_avatar_image.png")  # 你的头像路径

# 保存和恢复会话状态
def save_session(conv_name: str = None):
    chat_box.context_from_session(
        conv_name, exclude=["selected_page", "prompt", "cur_conv_name", "upload_image"]
    )

def restore_session(conv_name: str = None):
    chat_box.context_to_session(
        conv_name, exclude=["selected_page", "prompt", "cur_conv_name", "upload_image"]
    )

def rerun():
    save_session()
    st.rerun()

# 定义对话页面的UI布局
def dialogue_page():
    ctx = chat_box.context
    ctx.setdefault("uid", uuid.uuid4().hex)
    st.session_state.setdefault("cur_conv_name", chat_box.cur_chat_name)
    st.session_state.setdefault("last_conv_name", chat_box.cur_chat_name)

    if st.session_state.cur_conv_name != st.session_state.last_conv_name:
        save_session(st.session_state.last_conv_name)
        restore_session(st.session_state.cur_conv_name)
        st.session_state.last_conv_name = st.session_state.cur_conv_name

    # 会话框的侧边栏设置
    with st.sidebar:
        tab1, tab2 = st.tabs(["工具设置", "会话设置"])

        with tab1:
            use_agent = st.checkbox("启用Agent", help="请确保选择的模型具备Agent能力", key="use_agent")
            output_agent = st.checkbox("显示Agent过程", key="output_agent")

        with tab2:
            # 会话
            cols = st.columns(3)
            conv_names = chat_box.get_chat_names()

            conversation_name = sac.buttons(
                conv_names,
                label="当前会话：",
                key="cur_conv_name",
            )
            chat_box.use_chat_name(conversation_name)
            if cols[0].button("新建"):
                add_conv()

    # 显示聊天记录
    chat_box.output_messages()

    # 输入区域
    chat_input_placeholder = "请输入对话内容，换行请使用Shift+Enter。"
    with bottom():
        cols = st.columns([1, 0.2, 15, 1])
        if cols[-1].button(":wastebasket:", help="清空对话"):
            chat_box.reset_history()
            rerun()

        # 用户输入的对话框
        prompt = cols[2].chat_input(chat_input_placeholder, key="prompt")

    if prompt:
        chat_box.user_say(prompt)
        chat_box.ai_say("正在思考...")

# 会话管理函数
def add_conv():
    conv_names = chat_box.get_chat_names()
    i = len(conv_names) + 1
    while f"会话{i}" in conv_names:
        i += 1
    chat_box.use_chat_name(f"会话{i}")
    st.session_state["cur_conv_name"] = f"会话{i}"

# 主函数
if __name__ == "__main__":
    st.set_page_config(
        page_title="对话界面",
        layout="wide",
    )
    st.title("多功能对话系统")
    dialogue_page()
