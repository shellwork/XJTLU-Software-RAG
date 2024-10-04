import streamlit as st
import subprocess

# Frontend interface
st.title("Chroma Database Management")

# Delete the database
if st.button("Delete Existing Database"):
    try:
        subprocess.run(["python", "delete_database_script.py"], check=True)
        st.success("Database deleted successfully")
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to delete the database: {e}")

# Load new documents and update the database
if st.button("Load New Documents and Update Database"):
    try:
        subprocess.run(["python", "generate_data_store_script.py"], check=True)
        st.success("Database updated successfully")
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to load new documents: {e}")

# Load JSON documents and update the database
if st.button("Load JSON Documents and Update Database"):
    try:
        subprocess.run(["python", "generate_json_data_store_script.py"], check=True)
        st.success("JSON document database updated successfully")
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to load JSON documents: {e}")
