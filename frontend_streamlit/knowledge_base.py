import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import requests
from pathlib import Path

# 设置文件保存的主目录
UPLOAD_DIR = Path("knowledge_base")

# 确保上传目录存在
UPLOAD_DIR.mkdir(exist_ok=True)

def knowledge_base_page(api=None, is_lite=False):
    # 获取现有的知识库列表，从后端获取
    response = requests.get("http://localhost:8000/get_kb_list")
    if response.status_code == 200:
        kb_list = response.json()
    else:
        kb_list = {}

    kb_names = list(kb_list.keys())

    if "selected_kb_name" not in st.session_state:
        st.session_state["selected_kb_name"] = kb_names[0] if kb_names else "无知识库"

    # 选择知识库的下拉框
    selected_kb = st.selectbox(
        "请选择或新建知识库：",
        kb_names + ["新建知识库"],
        index=kb_names.index(st.session_state["selected_kb_name"]) if st.session_state["selected_kb_name"] in kb_names else 0
    )

    st.session_state["selected_kb_name"] = selected_kb

    # 如果选择了新建知识库，展示创建表单
    if selected_kb == "新建知识库":
        with st.form("新建知识库"):
            kb_name = st.text_input("新建知识库名称", placeholder="请输入新知识库名称")
            kb_info = st.text_input("知识库简介", placeholder="请输入知识库简介")

            vs_type = st.selectbox("向量库类型", ["类型1", "类型2"], index=0)
            embed_model = st.selectbox("Embeddings模型", ["模型1", "模型2"], index=0)

            submit_create_kb = st.form_submit_button("新建知识库")
            if submit_create_kb:
                if not kb_name:
                    st.error("知识库名称不能为空！")
                else:
                    st.success(f"成功创建知识库：{kb_name}")
                    # 调用后端接口创建知识库
                    create_kb_response = requests.post(
                        "http://localhost:8000/create_kb",
                        json={"kb_name": kb_name, "kb_info": kb_info, "vs_type": vs_type, "embed_model": embed_model}
                    )
                    if create_kb_response.status_code == 200:
                        st.success(f"知识库 {kb_name} 创建成功！")
                        update_query_params()
                    else:
                        st.error("创建知识库失败，请稍后再试。")

    else:
        # 展示已选知识库的详细信息
        st.write(f"当前选择的知识库：{selected_kb}")
        st.text_area("知识库简介", kb_list[selected_kb])

        # 获取知识库中的文档列表
        docs_response = requests.get(f"http://localhost:8000/get_kb_documents?kb_name={selected_kb}")
        if docs_response.status_code == 200:
            doc_details = pd.DataFrame(docs_response.json(), columns=["file_name"])
        else:
            doc_details = pd.DataFrame(columns=["file_name"])

        # 文件上传区域
        files = st.file_uploader("上传知识文件：", accept_multiple_files=True)
        if st.button("添加文件到知识库"):
            if files:
                upload_files(selected_kb, files)
                update_query_params()
            else:
                st.error("请先上传文件！")

        # 文件处理配置
        with st.expander("文件处理配置"):
            chunk_size = st.number_input("单段文本最大长度：", min_value=1, max_value=1000, value=100)
            chunk_overlap = st.number_input("相邻文本重合长度：", min_value=0, max_value=100, value=20)
            zh_title_enhance = st.checkbox("开启中文标题加强", value=False)

        # 知识库中文档的展示表格
        st.write(f"知识库 `{selected_kb}` 中已有文件：")
        gb = GridOptionsBuilder.from_dataframe(doc_details)
        gb.configure_pagination(paginationPageSize=5)
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        grid_options = gb.build()
        grid_response = AgGrid(doc_details, gridOptions=grid_options, height=200)

        # 删除选中文件的功能
        selected_files = grid_response["selected_rows"]
        if st.button("删除选中文件"):
            if selected_files:
                file_names = [file["file_name"] for file in selected_files]
                delete_response = requests.post(
                    "http://localhost:8000/delete_kb_files",
                    json={"kb_name": selected_kb, "files": file_names}
                )
                if delete_response.status_code == 200:
                    st.success("文件删除成功！")
                    update_query_params()
                else:
                    st.error("文件删除失败，请稍后再试。")
            else:
                st.warning("请先选择文件")

        st.divider()

        # 重建向量库的操作
        if st.button("依据源文件重建向量库"):
            rebuild_response = requests.post(f"http://localhost:8000/rebuild_vector_store?kb_name={selected_kb}")
            if rebuild_response.status_code == 200:
                st.success(f"向量库已成功为知识库 {selected_kb} 重建")
            else:
                st.error("向量库重建失败，请稍后再试。")

        if st.button("删除知识库", type="primary"):
            st.warning("删除知识库功能待实现")


def upload_files(kb_name, files):
    """将文件拷贝并根据后缀分类保存到相应目录"""
    for file in files:
        files_payload = {'files': (file.name, file.getvalue())}
        response = requests.post(
            f"http://localhost:8000/upload_files",  # 修复后的 API 路径
            files=files_payload,  # 传递文件内容
            data={"kb_name": kb_name}  # 使用 form-data 传递知识库名称
        )

        if response.status_code == 200:
            st.success(f"{file.name} 上传成功")
        else:
            st.error(f"文件 {file.name} 上传失败，错误信息: {response.text}")

# 在操作之后更新查询参数以刷新页面
def update_query_params():
    st.query_params.from_dict({"dummy": str(st.session_state.get("dummy", 0) + 1)})


if __name__ == "__main__":
    st.set_page_config(page_title="知识库管理", layout="wide")
    knowledge_base_page()
