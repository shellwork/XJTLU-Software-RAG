import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import requests
from pathlib import Path
# 设置文件保存的主目录
from config import UPLOAD_DIR

UPLOAD_DIR = Path(UPLOAD_DIR)
# 确保上传目录存在
UPLOAD_DIR.mkdir(exist_ok=True)


def knowledge_base_page():
    # 获取现有的知识库列表，从后端获取
    response = requests.get("http://localhost:8000/get_kb_list")
    if response.status_code == 200:
        kb_list = response.json()
    else:
        kb_list = {}

    kb_names = list(kb_list.keys())

    # 从 URL 查询参数中获取当前选中的知识库
    query_params = st.query_params.to_dict()
    selected_kb = query_params.get("selected_kb_name", kb_names[0] if kb_names else "无知识库")

    if "selected_kb_name" not in st.session_state:
        st.session_state["selected_kb_name"] = selected_kb

    # 选择知识库的下拉框
    selected_kb = st.selectbox(
        "请选择或新建知识库：",
        kb_names + ["新建知识库"],
        index=kb_names.index(st.session_state["selected_kb_name"]) if st.session_state[
                                                                          "selected_kb_name"] in kb_names else 0
    )

    st.session_state["selected_kb_name"] = selected_kb

    # 更新 URL 中的查询参数
    st.query_params.from_dict({"selected_kb_name": selected_kb})

    # 如果选择了新建知识库，展示创建表单
    if selected_kb == "新建知识库":
        with st.form("新建知识库"):
            kb_name = st.text_input("新建知识库名称", placeholder="请输入新知识库名称")
            kb_info = st.text_input("知识库简介", placeholder="请输入知识库简介")

            vs_type = st.selectbox("向量库类型", ["chroma", "类型2"], index=0)
            embed_model = st.selectbox("Embeddings模型", ["openai", "本地"], index=0)

            submit_create_kb = st.form_submit_button("新建知识库")
            if submit_create_kb:
                if not kb_name:
                    st.error("知识库名称不能为空！")
                else:
                    # 调用后端接口创建知识库，并传递选择的 embed_model 和 vs_type
                    create_kb_response = requests.post(
                        "http://localhost:8000/create_kb",
                        json={"kb_name": kb_name, "kb_info": kb_info, "vs_type": vs_type, "embed_model": embed_model}
                    )
                    if create_kb_response.status_code == 200:
                        st.success(f"知识库 {kb_name} 创建成功！")
                        st.session_state["selected_kb_name"] = kb_name
                        st.rerun()
                    else:
                        st.error("创建知识库失败，请稍后再试。")

    else:
        # 展示已选知识库的详细信息
        st.write(f"当前选择的知识库：{selected_kb}")
        st.text_area("知识库简介", kb_list[selected_kb])

        # 获取知识库中的文档列表
        docs_response = requests.get(f"http://localhost:8000/get_kb_documents?kb_name={selected_kb}")
        if docs_response.status_code == 200:
            doc_details = pd.DataFrame(docs_response.json())
        else:
            doc_details = pd.DataFrame(columns=["category", "file_name"])

        # 文件上传区域
        files = st.file_uploader("上传知识文件：", accept_multiple_files=True)

        # 文件处理配置
        with st.expander("文件处理配置"):
            chunk_size = st.number_input("单段文本最大长度：", min_value=1, max_value=1000, value=100)
            chunk_overlap = st.number_input("相邻文本重合长度：", min_value=0, max_value=100, value=20)
            zh_title_enhance = st.checkbox("开启中文标题加强", value=False)

        if st.button("添加文件到知识库"):
            if files:
                # 将所有文件与配置参数通过请求发送至 API
                files_payload = [('files', (file.name, file.read(), file.type)) for file in files]

                # 额外的配置参数
                data_payload = {
                    "kb_name": selected_kb,
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                    "zh_title_enhance": zh_title_enhance
                }

                response = requests.post(
                    "http://localhost:8000/upload_files",
                    files=files_payload,
                    data=data_payload
                )

                if response.status_code == 200 and response.json().get("status") == "success":
                    st.success(f"{len(files)} 文件上传成功至知识库 {selected_kb}")
                    st.rerun()
                else:
                    st.error(f"文件上传失败，错误信息: {response.text}")
            else:
                st.error("请先上传文件！")

        # 知识库中文档的展示表格
        st.write(f"知识库 `{selected_kb}` 中已有文件：")
        if not doc_details.empty:
            # 添加显示的列: category, file_name, file_size, chunk_size, chunk_overlap
            doc_details["file_size_kb"] = (doc_details["file_size"] / 1024).round(2)  # 将文件大小转换为KB
            gb = GridOptionsBuilder.from_dataframe(doc_details)
            # 设置表格中显示的列和列名
            gb.configure_column("category", header_name="类别")
            gb.configure_column("file_name", header_name="文件名")
            gb.configure_column("file_size_kb", header_name="文件大小 (KB)",
                                type=["numericColumn", "numberColumnFilter"])
            gb.configure_column("chunk_size", header_name="分块大小")
            gb.configure_column("chunk_overlap", header_name="分块重叠")

            # 设置分页和选择功能
            gb.configure_pagination(paginationPageSize=5)
            gb.configure_selection(selection_mode="multiple", use_checkbox=True)

            grid_options = gb.build()
            grid_response = AgGrid(doc_details, gridOptions=grid_options, height=200)

            # 删除选中文件的功能
            selected_files = grid_response["selected_rows"]

            # 确保 selected_files 是一个列表
            if isinstance(selected_files, pd.DataFrame):
                selected_files = selected_files.to_dict(orient='records')

            # 确认 selected_files 是列表后，进行删除操作
            if st.button("删除选中文件"):
                if selected_files:
                    files_to_delete = [
                        {"category": file.get("category", ""), "file_name": file.get("file_name", "")}
                        for file in selected_files
                    ]
                    st.write(f"准备删除的文件：{files_to_delete}")
                    st.write(f"知识库：{selected_kb}")

                    delete_response = requests.post(
                        "http://localhost:8000/delete_kb_files",
                        json={"kb_name": selected_kb, "files": files_to_delete}
                    )

                    # 检查响应状态并打印响应内容
                    if delete_response.status_code == 200:
                        st.success("文件删除成功！")
                        st.rerun()
                    else:
                        st.error(f"文件删除失败，错误信息: {delete_response.text}")
                else:
                    st.warning("请先选择文件")
        else:
            st.write("该知识库中暂无文件。")

        st.divider()

        # 重建向量库的操作
        action = st.checkbox("是否重建向量库?", help="勾选则删除已有并重新构建数据库", key="action")
        if st.button("依据源文件更新向量库"):
            rebuild_response = requests.post(f"http://localhost:8000/rebuild_vector_store?kb_name={selected_kb}&action={action}")
            if rebuild_response.status_code == 200:
                st.success(f"向量库已成功为知识库 {selected_kb} 更新")
            else:
                st.error("向量库更新失败，请稍后再试。")


        if st.button("删除整个知识库"):
            if st.checkbox("确认删除整个知识库？"):
                st.write(selected_kb)  # 打印当前选择的知识库，便于调试
                delete_kb_response = requests.post(
                    "http://localhost:8000/delete_kb",
                    data={"kb_name": selected_kb}
                )
                # 检查后端的响应状态
                if delete_kb_response.status_code == 200 and delete_kb_response.json().get("status") == "success":
                    st.success(delete_kb_response.json().get("message"))
                    # 重置 session 和 query params
                    st.session_state["selected_kb_name"] = ""
                    st.query_params.clear()
                    st.rerun()
                else:
                    st.error(f"删除知识库失败: {delete_kb_response.json().get('message')}")
            else:
                st.info(f"请勾选确认删除！")



if __name__ == "__main__":
    st.set_page_config(page_title="知识库管理", layout="wide")
    knowledge_base_page()
