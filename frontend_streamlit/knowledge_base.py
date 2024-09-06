import os
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# 主要实现知识库的UI界面，后续接入后端时再进行修改

def knowledge_base_page(api=None, is_lite=False):
    # 获取现有的知识库列表（这里为接入后端时预留的部分）
    # 后端接入：获取知识库详情
    kb_list = {"知识库1": "介绍1", "知识库2": "介绍2"}
    kb_names = list(kb_list.keys())

    if "selected_kb_name" not in st.session_state:
        st.session_state["selected_kb_name"] = kb_names[0]

    # 选择知识库的下拉框
    selected_kb = st.selectbox(
        "请选择或新建知识库：",
        kb_names + ["新建知识库"],
        index=kb_names.index(st.session_state["selected_kb_name"]) if st.session_state["selected_kb_name"] in kb_names else 0
    )

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
                    # 后端接入：调用接口创建知识库

    else:
        # 展示已选知识库的详细信息
        st.write(f"当前选择的知识库：{selected_kb}")
        st.text_area("知识库简介", kb_list[selected_kb])

        # 文件上传区域
        files = st.file_uploader("上传知识文件：", accept_multiple_files=True)
        if st.button("添加文件到知识库"):
            if files:
                st.success(f"成功上传 {len(files)} 个文件")
                # 后端接入：将文件上传到指定知识库
            else:
                st.error("请先上传文件！")

        # 文件处理配置
        with st.expander("文件处理配置"):
            chunk_size = st.number_input("单段文本最大长度：", min_value=1, max_value=1000, value=100)
            chunk_overlap = st.number_input("相邻文本重合长度：", min_value=0, max_value=100, value=20)
            zh_title_enhance = st.checkbox("开启中文标题加强", value=False)

        # 知识库中文档的展示表格（此处为示例数据）
        doc_details = pd.DataFrame({
            "No": [1, 2],
            "file_name": ["file1.txt", "file2.txt"],
            "document_loader": ["loader1", "loader2"],
            "docs_count": [5, 8],
            "in_folder": ["✓", "✓"],
            "in_db": ["✓", "×"]
        })

        st.write(f"知识库 `{selected_kb}` 中已有文件：")
        gb = GridOptionsBuilder.from_dataframe(doc_details)
        gb.configure_pagination(paginationPageSize=5)
        grid_options = gb.build()
        grid_response = AgGrid(doc_details, gridOptions=grid_options, height=200)

        # 操作按钮
        cols = st.columns(4)
        if cols[0].button("下载选中文档"):
            # 后端接入：下载选中文档的操作
            st.info("文档下载功能待实现")

        if cols[1].button("重新添加至向量库"):
            # 后端接入：重新添加至向量库的操作
            st.info("重新添加至向量库功能待实现")

        if cols[2].button("从向量库删除"):
            # 后端接入：从向量库删除操作
            st.info("从向量库删除功能待实现")

        if cols[3].button("从知识库中删除"):
            # 后端接入：从知识库中删除操作
            st.info("从知识库中删除功能待实现")

        st.divider()

        # 重建向量库的操作
        if st.button("依据源文件重建向量库"):
            st.info("向量库重建功能待实现")

        if st.button("删除知识库", type="primary"):
            st.warning("删除知识库功能待实现")
