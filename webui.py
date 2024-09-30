import sys
import streamlit as st
import streamlit_antd_components as sac
from frontend_streamlit.dialogue import dialogue_page as custom_dialogue_page  # Import multi-functional dialogue page
# from frontend_streamlit.kb_chat import kb_chat as custom_kb_chat  # Import RAG dialogue page
from frontend_streamlit.knowledge_base import knowledge_base_page as custom_knowledge_base_page  # Import knowledge base management page
from config import __version__
import base64

# Function to call multi-functional dialogue
def dialogue_page(api=None, is_lite=False):
    custom_dialogue_page()  # Call the previously implemented multi-functional dialogue page

# Function to call RAG dialogue
# def kb_chat(api=None):
#     custom_kb_chat()  # Call the RAG dialogue page

# Function to call knowledge base management
def knowledge_base_page(api=None, is_lite=False):
    custom_knowledge_base_page()  # Call the knowledge base management page

# Page startup logic
if __name__ == "__main__":
    is_lite = "lite" in sys.argv  # Lite mode can be removed later

    # Page configuration
    st.set_page_config(
        page_title="XJTLU-Software Chatparts",
        page_icon="frontend_streamlit/img/icon1.png",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/shellwork/XJTLU-Software-RAG/",
            "Report a bug": "https://github.com/shellwork/XJTLU-Software-RAG/issues",
            "About": f"Welcome to XJTLU-Software Chatparts {__version__}!",
        },
        layout="centered",
    )

    # Custom settings for page width and style
    st.markdown(
        """
        <style>

        /* Define slide-in animation, suitable for elements sliding in upwards */
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

        /* Define slide-in-from-top animation */
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

        /* Apply slide-in animation to main content area */
        .block-container {
            padding-top: 45px;
            animation: slide-in 0.4s ease-out;
        }

        /* Apply slide-in-from-top animation to sidebar */
        [data-testid="stSidebarUserContent"] {
            padding-top: 40px;
            animation: slide-in-from-top 0.4s ease-out;
        }

        /* Entry animation for bottom container */
        [data-testid="stBottomBlockContainer"] {
            padding-bottom: 20px;
            animation: slide-in 0.4s ease-out;
        }

        /* Add animation effects to menu items */
        .sac-menu-item {
            animation: slide-in-from-top 0.3s ease-in-out;
        }

        /* Scaling effect on hover for menu items, and change color to blue */
        .sac-menu-item:hover {
            animation: pulse 0.2s;
            color: #3c5494;  /* Blue on hover */
        }

        /* Define color change to blue when hovering over all icons */
        .icon:hover {
            color: #3c5494 !important; /* Force color to blue on hover */
        }

        /* Define pulse animation */
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


    def set_bg(main_bg_path):
        # 获取文件扩展名
        main_bg_ext = main_bg_path.split('.')[-1]

        # 读取并编码图片为 base64
        with open(main_bg_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()

        # 使用自定义的 CSS 设置背景
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url(data:image/{main_bg_ext};base64,{encoded_image});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )


    # 调用
    set_bg('frontend_streamlit/img/background.png')


    # Sidebar configuration
    with st.sidebar:
        st.image("frontend_streamlit/img/complete_icon.png", use_column_width=True)

        # Version information
        st.caption(f"""<p align="right">Current version: {__version__}</p>""", unsafe_allow_html=True)

        # Menu
        selected_page = sac.menu(
            [
                sac.MenuItem("Multi-functional Dialogue", icon="chat"),
                # sac.MenuItem("RAG Dialogue (Under Development)", icon="database"),
                sac.MenuItem("Knowledge Base Management", icon="hdd-stack"),
            ],
            key="selected_page",
            open_index=0,
        )

        sac.divider()

    # Page display logic
    if selected_page == "Knowledge Base Management":
        knowledge_base_page(api=None, is_lite=is_lite)  # Will integrate actual API later
    # elif selected_page == "RAG Dialogue":
    #     kb_chat(api=None)
    else:
        dialogue_page(api=None, is_lite=is_lite)
