import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import requests
from pathlib import Path
# Set the main directory for file saving
from config import UPLOAD_DIR
from frontend_streamlit.dialogue import get_local_models, get_api_models

UPLOAD_DIR = Path(UPLOAD_DIR)
# Ensure the upload directory exists
UPLOAD_DIR.mkdir(exist_ok=True)


def knowledge_base_page():
    # Fetch the existing knowledge base list from the backend
    response = requests.get("http://localhost:8000/get_kb_list")
    if response.status_code == 200:
        kb_list = response.json()
    else:
        kb_list = {}

    kb_names = list(kb_list.keys())

    # Get the currently selected knowledge base from the URL query parameters
    query_params = st.query_params.to_dict()
    selected_kb = query_params.get("selected_kb_name", kb_names[0] if kb_names else "No Knowledge Base")

    if "selected_kb_name" not in st.session_state:
        st.session_state["selected_kb_name"] = selected_kb

    # Dropdown to select or create a knowledge base
    selected_kb = st.selectbox(
        "Please select or create a knowledge base:",
        kb_names + ["Create New Knowledge Base"],
        index=kb_names.index(st.session_state["selected_kb_name"]) if st.session_state[
                                                                          "selected_kb_name"] in kb_names else 0
    )

    with st.sidebar:
        st.sidebar.header("Embedding Model Settings")

        try:
            settings_response = requests.get(f"http://localhost:8000/api/get_vector_model?kb_name={selected_kb}")
            if settings_response.status_code == 200:
                current_settings = settings_response.json()
            else:
                st.sidebar.error("无法获取当前向量模型设置")
                current_settings = {"use_local": False, "provider": "openai", "embed_model": "Default"}
        except Exception as e:
            st.sidebar.error(f"获取当前设置时出错: {e}")
            current_settings = {"use_local": False, "provider": "openai", "embed_model": "Default"}

        use_local_model = st.checkbox("Enable Local Model", help="Use local model for inference when enabled",
                                      key="use_local_model")

        if use_local_model:
            available_eb_models = get_local_models().get("local_eb_models")
            eb_model_type = "Local Embedding Model"
        else:
            providers = ["openai", "qwen"]
            providers = st.selectbox("Seclect model providers", providers, key="providers")
            available_eb_models = get_api_models(providers).get("local_eb_models")
            eb_model_type = "API Embedding Model"
        embed_model = st.selectbox(f"Select {eb_model_type}", available_eb_models, key="selected_eb_model")
        # 自动提交设置
        submit = st.sidebar.button("Save embedding model settings")

        if submit:
            payload = {
                "kb_name": selected_kb,
                "use_local": use_local_model,
                "provider": providers,
                "embed_model": embed_model
            }
            try:
                response = requests.post(
                    "http://localhost:8000/api/update_vector_model",
                    json=payload
                )
                if response.status_code == 200 and response.json().get("status") == "success":
                    st.sidebar.success("Vector model settings updated successfully")
                    st.rerun()
                else:
                    error_message = response.json().get("message", "Unknown error")
                    st.sidebar.error(f"Update failed: {error_message}")
            except Exception as e:
                st.sidebar.error(f"Request failed: {e}")

        # Display the current global vector model settings
        st.sidebar.markdown("### Current Vector Model Settings")
        st.sidebar.write(f"**Model Type:** {'Local Model' if current_settings['use_local'] else 'API Model'}")
        st.sidebar.write(f"**Provider:** {current_settings['provider']}")
        st.sidebar.write(f"**Model:** {current_settings['embed_model']}")



    st.session_state["selected_kb_name"] = selected_kb

    # Update the query parameters in the URL
    st.query_params.from_dict({"selected_kb_name": selected_kb})

    # If "Create New Knowledge Base" is selected, display the creation form
    if selected_kb == "Create New Knowledge Base":
        with st.form("Create New Knowledge Base"):
            kb_name = st.text_input("New Knowledge Base Name", placeholder="Enter the new knowledge base name")
            kb_info = st.text_input("Knowledge Base Description", placeholder="Enter the knowledge base description")

            vs_type = st.selectbox("Vector Store Type", ["chroma", "Type 2"], index=0)
            local = st.checkbox("Use local embedding model", help="Use local model for inference when enabled")
            provider = st.selectbox("Embeddings Model Provider", ["openai", "qwen"], index=0)
            if provider == "openai":
                embed_model = st.selectbox("Embeddings Model", ["Default"], index=0)
            elif provider == "qwen":
                embed_model = st.selectbox("Embeddings Model", [
                    "text-embedding-v1",
                    # "text-embedding-async-v1",
                    "text-embedding-v2",
                    # "text-embedding-async-v2",
                    # "text-embedding-v3"
                ], index=0)
            else:
                st.error("Please choose provider first")
            submit_create_kb = st.form_submit_button("Create Knowledge Base")
            if submit_create_kb:
                if not kb_name:
                    st.error("Knowledge base name cannot be empty!")
                else:
                    # Call the backend API to create a knowledge base, passing the selected embed_model and vs_type
                    create_kb_response = requests.post(
                        "http://localhost:8000/create_kb",
                        json={"kb_name": kb_name, "kb_info": kb_info, "vs_type": vs_type, "embed_model": embed_model,
                              "provider": provider, "local": local}
                    )
                    if create_kb_response.status_code == 200:
                        st.success(f"Knowledge base {kb_name} created successfully!")
                        st.session_state["selected_kb_name"] = kb_name
                        st.rerun()
                    else:
                        st.error("Failed to create knowledge base, please try again later.")

    else:
        # Display details of the selected knowledge base
        st.write(f"Currently selected knowledge base: {selected_kb}")
        st.text_area("Knowledge Base Description", kb_list[selected_kb])

        # Fetch the document list in the knowledge base
        docs_response = requests.get(f"http://localhost:8000/get_kb_documents?kb_name={selected_kb}")
        if docs_response.status_code == 200:
            doc_details = pd.DataFrame(docs_response.json())
        else:
            doc_details = pd.DataFrame(columns=["category", "file_name"])

        # File upload section
        files = st.file_uploader("Upload Knowledge Files:", accept_multiple_files=True)

        # File processing configuration
        with st.expander("File Processing Configuration"):
            chunk_size = st.number_input("Maximum text length per chunk:", min_value=1, max_value=1000, value=100)
            chunk_overlap = st.number_input("Overlap length between adjacent chunks:", min_value=0, max_value=100,
                                            value=20)
            # zh_title_enhance = st.checkbox("Enable Chinese Title Enhancement(not completed yet)", value=False)

        if st.button("Add Files to Knowledge Base"):
            if files:
                # Send all files and configuration parameters to the API via a request
                files_payload = [('files', (file.name, file.read(), file.type)) for file in files]

                # Additional configuration parameters
                data_payload = {
                    "kb_name": selected_kb,
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                    "zh_title_enhance": False  # zh_title_enhance still not completed
                }

                response = requests.post(
                    "http://localhost:8000/upload_files",
                    files=files_payload,
                    data=data_payload
                )

                if response.status_code == 200 and response.json().get("status") == "success":
                    st.success(f"{len(files)} files uploaded successfully to knowledge base {selected_kb}")
                    st.rerun()
                else:
                    st.error(f"File upload failed, error message: {response.text}")
            else:
                st.error("Please upload files first!")

        # Display the table of documents in the knowledge base
        st.write(f"Existing files in knowledge base `{selected_kb}`:")
        if not doc_details.empty:
            # Add displayed columns: category, file_name, file_size, chunk_size, chunk_overlap
            doc_details["file_size_kb"] = (doc_details["file_size"] / 1024).round(2)  # Convert file size to KB
            gb = GridOptionsBuilder.from_dataframe(doc_details)
            # Configure columns and their headers in the table
            gb.configure_column("category", header_name="Category")
            gb.configure_column("file_name", header_name="File Name")
            gb.configure_column("file_size_kb", header_name="File Size (KB)",
                                type=["numericColumn", "numberColumnFilter"])
            gb.configure_column("chunk_size", header_name="Chunk Size")
            gb.configure_column("chunk_overlap", header_name="Chunk Overlap")

            # Configure pagination and selection features
            gb.configure_pagination(paginationPageSize=5)
            gb.configure_selection(selection_mode="multiple", use_checkbox=True)

            grid_options = gb.build()
            grid_response = AgGrid(doc_details, gridOptions=grid_options, height=200)

            # Functionality to delete selected files
            selected_files = grid_response["selected_rows"]

            # Ensure selected_files is a list
            if isinstance(selected_files, pd.DataFrame):
                selected_files = selected_files.to_dict(orient='records')

            # Once selected_files is confirmed to be a list, proceed with deletion
            if st.button("Delete Selected Files"):
                if selected_files:
                    files_to_delete = [
                        {"category": file.get("category", ""), "file_name": file.get("file_name", "")}
                        for file in selected_files
                    ]
                    st.write(f"Files to be deleted: {files_to_delete}")
                    st.write(f"Knowledge Base: {selected_kb}")

                    delete_response = requests.post(
                        "http://localhost:8000/delete_kb_files",
                        json={"kb_name": selected_kb, "files": files_to_delete}
                    )

                    # Check the response status and print the response content
                    if delete_response.status_code == 200:
                        st.success("Files deleted successfully!")
                        st.rerun()
                    else:
                        st.error(f"File deletion failed, error message: {delete_response.text}")
                else:
                    st.warning("Please select files first")
        else:
            st.write("No files in this knowledge base.")

        st.divider()

        # Rebuild the vector store
        action = st.checkbox("Rebuild the vector store?", help="Check to delete and rebuild the database", key="action")
        if st.button("Update Vector Store Based on Source Files"):
            rebuild_response = requests.post(
                f"http://localhost:8000/rebuild_vector_store?kb_name={selected_kb}&action={action}")
            if rebuild_response.status_code == 200:
                st.success(f"Vector store successfully updated for knowledge base {selected_kb}")
            else:
                st.error("Failed to update vector store, please try again later.")

        if st.button("Delete Entire Knowledge Base"):
            if st.checkbox("Confirm deletion of the entire knowledge base?"):
                st.write(selected_kb)  # Print the currently selected knowledge base for debugging
                delete_kb_response = requests.post(
                    "http://localhost:8000/delete_kb",
                    data={"kb_name": selected_kb}
                )
                # Check the backend's response status
                if delete_kb_response.status_code == 200 and delete_kb_response.json().get("status") == "success":
                    st.success(delete_kb_response.json().get("message"))
                    # Reset session and query params
                    st.session_state["selected_kb_name"] = ""
                    st.query_params.clear()
                    st.rerun()
                else:
                    st.error(f"Failed to delete knowledge base: {delete_kb_response.json().get('message')}")
            else:
                st.info("Please check the confirmation box!")


if __name__ == "__main__":
    st.set_page_config(page_title="Knowledge Base Management", layout="wide")
    knowledge_base_page()
