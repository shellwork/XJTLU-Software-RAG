import streamlit as st
import subprocess
from frontend_streamlit.query import query_chroma  # 从 query.py 导入查询函数

# 设置页面标题和布局
st.set_page_config(
    page_title="Chroma 数据库系统",
    page_icon=":books:",
    layout="wide"
)

# 定义主函数
def main():

    # 页面标题
    st.title("Chroma 数据库系统")

    # 侧边栏选项，用于选择不同的功能
    options = ["Chroma 数据库查询", "Chroma 数据库管理"]
    choice = st.sidebar.selectbox("选择功能", options)

    # 根据选择展示不同的页面
    if choice == "Chroma 数据库查询":
        show_query_page()  # 显示查询页面
    elif choice == "Chroma 数据库管理":
        show_database_management_page()  # 显示数据库管理页面

# 显示查询页面
def show_query_page():
    st.subheader("Chroma 数据库查询")

    # 输入查询
    query_text = st.text_input("请输入查询内容")
    model_name = st.selectbox("选择模型", options=["gpt-3.5-turbo", "gpt-4"])

    # 执行查询按钮
    if st.button("执行查询"):
        if query_text:
            # 调用 query.py 中的查询函数
            response, sources = query_chroma(query_text, model_name)
            if response:
                st.write(f"回答：{response}")
                st.write(f"来源：{', '.join(sources)}")
            else:
                st.write("未找到相关结果或相似度不足")
        else:
            st.error("请输入查询内容")

# 显示数据库管理页面
def show_database_management_page():
    st.subheader("Chroma 数据库管理")

    # 删除数据库按钮
    if st.button("删除现有数据库"):
        try:
            # 调用后端删除数据库的脚本
            subprocess.run(["python", "./server/create_database.py"], check=True)
            st.success("数据库已删除")
        except subprocess.CalledProcessError as e:
            st.error(f"删除数据库失败: {e}")

    # 加载新文档并更新数据库按钮
    if st.button("加载新文档并更新数据库"):
        try:
            # 调用后端加载新文档的脚本
            subprocess.run(["python", "./server/create_database.py"], check=True)
            st.success("数据库已更新")
        except subprocess.CalledProcessError as e:
            st.error(f"加载新文档失败: {e}")

    # 加载 JSON 文档并更新数据库按钮
    if st.button("加载 JSON 文档并更新数据库"):
        try:
            # 调用后端加载 JSON 文档的脚本
            subprocess.run(["python", "./server/create_database.py"], check=True)
            st.success("JSON 文档数据库已更新")
        except subprocess.CalledProcessError as e:
            st.error(f"加载 JSON 文档失败: {e}")

# 运行主函数
if __name__ == "__main__":
    main()
