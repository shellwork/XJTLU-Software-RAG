import sys
import streamlit as st
import streamlit_antd_components as sac
from frontend_streamlit.dialogue import dialogue_page as custom_dialogue_page  # 导入多功能对话页面
from frontend_streamlit.kb_chat import kb_chat as custom_kb_chat  # 导入RAG对话页面
from frontend_streamlit.knowledge_base import knowledge_base_page as custom_knowledge_base_page  # 导入知识库管理页面

__version__ = "1.0.0"

# 调用多功能对话的函数
def dialogue_page(api=None, is_lite=False):
    custom_dialogue_page()  # 调用之前实现的多功能对话页面

# 调用RAG对话的函数
def kb_chat(api=None):
    custom_kb_chat()  # 调用RAG对话页面

# 调用知识库管理的函数
def knowledge_base_page(api=None, is_lite=False):
    custom_knowledge_base_page()  # 调用知识库管理页面

# 页面启动逻辑
if __name__ == "__main__":
    is_lite = "lite" in sys.argv  # 后续可移除 lite 模式

    # 页面配置
    st.set_page_config(
        page_title="XJTLU-Software Chatparts",
        page_icon="frontend_streamlit/img/icon.png",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/shellwork/XJTLU-Software-RAG/",
            "Report a bug": "https://github.com/shellwork/XJTLU-Software-RAG/issues",
            "About": f"Welcome to XJTLU-Software Chatparts {__version__}！",
        },
        layout="centered",
    )

    # 用于页面宽度和样式的自定义设置
    st.markdown(
        """
        <style>
        /* 定义slide-in动画，适用于向上滑动进入的元素 */
        @keyframes slide-in {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0px);
            }
        }

        /* 定义从顶部滑入的动画 */
        @keyframes slide-in-from-top {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0px);
            }
        }

        /* 应用 slide-in 动画到主要内容区域 */
        .block-container {
            padding-top: 45px;
            animation: slide-in 0.4s ease-out;
        }

        /* 应用 slide-in-from-top 动画到侧边栏 */
        [data-testid="stSidebarUserContent"] {
            padding-top: 40px;
            animation: slide-in-from-top 0.4s ease-out;
        }

        /* 底部容器的进入动画 */
        [data-testid="stBottomBlockContainer"] {
            padding-bottom: 20px;
            animation: slide-in 0.4s ease-out;
        }

        /* 为菜单项添加动画效果 */
        .sac-menu-item {
            animation: slide-in-from-top 0.3s ease-in-out;
        }

        /* 菜单项悬停时的缩放效果，并修改颜色为蓝色 */
        .sac-menu-item:hover {
            animation: pulse 0.2s;
            color: #3c5494;  /* 悬浮时的蓝色 */
        }

        /* 定义所有图标悬浮时的颜色变化为蓝色 */
        .icon:hover {
            color: #3c5494 !important; /* 强制将悬浮时颜色变为蓝色 */
        }

        /* pulse动画定义 */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        [data-testid="stSidebarUserContent"] {
            padding-top: 40px;
        }

        .block-container {
            padding-top: 45px;
        }

        [data-testid="stBottomBlockContainer"] {
            padding-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 侧边栏配置
    with st.sidebar:
        st.image("frontend_streamlit/img/complete_icon.png", use_column_width=True)

        # 版本信息
        st.caption(f"""<p align="right">当前版本：{__version__}</p>""", unsafe_allow_html=True)

        # 菜单
        selected_page = sac.menu(
            [
                sac.MenuItem("多功能对话", icon="chat"),
                sac.MenuItem("RAG 对话", icon="database"),
                sac.MenuItem("知识库管理", icon="hdd-stack"),
            ],
            key="selected_page",
            open_index=0,
        )

        sac.divider()

    # 页面显示逻辑
    if selected_page == "知识库管理":
        knowledge_base_page(api=None, is_lite=is_lite)  # 后续将会接入实际 API
    elif selected_page == "RAG 对话":
        kb_chat(api=None)
    else:
        dialogue_page(api=None, is_lite=is_lite)
