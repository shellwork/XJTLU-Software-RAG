import streamlit as st
import subprocess

# 前端界面
st.title("Chroma 数据库管理")

# 删除数据库
if st.button("删除现有数据库"):
    try:
        subprocess.run(["python", "delete_database_script.py"], check=True)
        st.success("数据库已删除")
    except subprocess.CalledProcessError as e:
        st.error(f"删除数据库失败: {e}")

# 加载新文档并更新数据库
if st.button("加载新文档并更新数据库"):
    try:
        subprocess.run(["python", "generate_data_store_script.py"], check=True)
        st.success("数据库已更新")
    except subprocess.CalledProcessError as e:
        st.error(f"加载新文档失败: {e}")

# 加载JSON文档并更新数据库
if st.button("加载 JSON 文档并更新数据库"):
    try:
        subprocess.run(["python", "generate_json_data_store_script.py"], check=True)
        st.success("JSON 文档数据库已更新")
    except subprocess.CalledProcessError as e:
        st.error(f"加载 JSON 文档失败: {e}")