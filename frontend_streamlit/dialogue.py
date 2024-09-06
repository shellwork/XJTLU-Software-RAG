import streamlit as st
import streamlit_antd_components as sac
from streamlit_chatbox import ChatBox
import requests
import uuid
from streamlit_extras.bottom_container import bottom
import os

# 初始化ChatBox
chat_box = ChatBox(assistant_avatar="frontend_streamlit/img/icon.png")  # 替换为你的头像路径

# 获取本地模型
def get_local_models():
    """
    获取本地模型列表，假设所有本地模型文件夹存储在 'local_models/' 目录中
    """
    local_models_dir = 'local_models/'  # 假设本地模型存储路径
    if os.path.exists(local_models_dir):
        return [f.name for f in os.scandir(local_models_dir) if f.is_dir()]
    return []

# 获取API模型
def get_api_models():
    """
    获取API可用模型列表
    """
    return ["gpt-3.5-turbo", "gpt-4", "anthropic", "cohere"]  # 假设API模型列表

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

# 调用后端的API
def call_backend(prompt, tools=None, model="default", use_self_model=False):
    try:
        response = requests.post(
            "http://localhost:8000/api/chat",  # 替换为后端的API路径
            json={"prompt": prompt, "tools": tools, "model": model, "use_self_model": use_self_model}
        )
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析JSON响应
        return data.get("response", "AI未能生成回复。")  # 获取AI的回复
    except requests.RequestException as e:
        st.error(f"请求后端服务时出错: {e}")
        return "请求后端服务时发生错误。"

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

    # 侧边栏设置
    with st.sidebar:
        tab2, tab1 = st.tabs(["会话", "设置"])

        with tab1:
            # 启用本地模型复选框
            use_local_model = st.checkbox("启用本地模型", help="启用后将使用本地模型推理", key="use_local_model")
            use_self_model = st.checkbox("启用模型对话", help="启用后将引入大模型自身对话性能", key="use_self_model")

            # 根据是否启用本地模型，动态显示可选模型
            if use_local_model:
                available_models = get_local_models()
                model_type = "本地模型"
            else:
                available_models = get_api_models()
                model_type = "API模型"

            # 模型选择下拉框
            selected_model = st.selectbox(f"选择{model_type}", available_models, key="selected_model")

            # 工具选择
            tools = st.multiselect("选择工具", ["工具1", "工具2", "工具3"], key="selected_tools")

        with tab2:
            # 显示对话的创建和删除
            st.write("对话管理")

            cols = st.columns(2)
            with cols[0]:
                if st.button("新建对话"):
                    add_conv()

            with cols[1]:
                if st.button("删除对话"):
                    delete_conv()

            conv_names = chat_box.get_chat_names()

            # 显示每个会话的按钮
            conversation_name = sac.buttons(
                conv_names,
                label="当前会话：",
                key="cur_conv_name",
            )
            chat_box.use_chat_name(conversation_name)

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

    # 处理用户输入
    if prompt and prompt.strip():  # 检查输入不为空
        chat_box.user_say(prompt.strip())  # 去除输入的空格
        # 调用后端API，获取AI回复
        ai_response = call_backend(prompt.strip(), tools=st.session_state.get("selected_tools", []), model=st.session_state.get("selected_model"), use_self_model=st.session_state.get("use_self_model"))
        chat_box.ai_say(ai_response)  # 显示AI回复

# 会话管理函数：新增对话
def add_conv():
    conv_names = chat_box.get_chat_names()
    i = len(conv_names) + 1
    new_conv_name = f"会话{i}"

    # 避免重复会话名称
    while new_conv_name in conv_names:
        i += 1
        new_conv_name = f"会话{i}"

    # 使用st.session_state的回调函数机制来更新会话名称
    if "cur_conv_name" in st.session_state:
        st.session_state.cur_conv_name = new_conv_name  # 更新当前会话名称
        chat_box.use_chat_name(new_conv_name)
    else:
        st.session_state.cur_conv_name = new_conv_name
        chat_box.use_chat_name(new_conv_name)

    # 重新运行以更新页面显示
    rerun()

# 会话管理函数：删除对话
def delete_conv():
    conv_name_to_delete = st.session_state.cur_conv_name
    conv_names = chat_box.get_chat_names()

    if len(conv_names) > 1:  # 确保至少有一个会话保留
        chat_box.del_chat_name(conv_name_to_delete)

        # 切换到其他对话
        st.session_state.cur_conv_name = conv_names[0] if conv_name_to_delete == conv_names[-1] else conv_names[-1]

        # 重新运行以更新页面显示
        rerun()
    else:
        st.warning("至少保留一个会话！")

# 预留函数：自动生成会话标题
def auto_generate_conv_name():
    # 在后端模型接入后，调用API自动生成对话名称
    return "自动生成的对话标题"  # 替换为实际逻辑

# 主函数
if __name__ == "__main__":
    st.set_page_config(
        page_title="对话界面",
        layout="wide",
    )
    st.title("多功能对话系统")
    dialogue_page()
