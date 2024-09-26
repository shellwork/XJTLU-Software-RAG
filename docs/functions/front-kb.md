# Frontend design of Knowledgebase management

This file is a Streamlit application for managing a knowledge base, featuring multiple functionalities such as displaying knowledge bases, uploading files, and creating new knowledge bases.

## Key components:

### 1. Basic Setup:

The application imports `streamlit` for building the user interface, `pandas` for handling tabular data, `AgGrid` for displaying documents in the knowledge base, and `requests` for communicating with the backend API.

`UPLOAD_DIR` is defined as the directory for file uploads, ensuring its existence through the `Path` module.

### 2. Knowledge Base Page Display and Selection:

Initially, it fetches the current list of knowledge bases via an API request (`requests.get("http://localhost:8000/get_kb_list"`)) and stores it in `kb_list` for user selection.

Users can choose from existing knowledge bases or select "Create New Knowledge Base" to set up a new one.

### 3. Creating a New Knowledge Base:

If the user selects "Create New Knowledge Base," a form is presented to enter the knowledge base name, description, vector store type (`vs_type`), and embedding model (`embed_model`).

Upon submission, a POST request (`requests.post`) is sent to the backend to create the knowledge base, and the page refreshes upon successful creation.

### 4. Displaying Knowledge Base Information:

Once a knowledge base is selected, its detailed information is displayed, including the description and a list of existing documents.

The document list is retrieved via an API request (`requests.get("http://localhost:8000/get_kb_documents?kb_name={selected_kb}")`) and presented in a table format using `AgGrid`.

### 5. File Upload and Processing:

Users can upload multiple files using `st.file_uploader`, along with configuring processing parameters such as maximum segment length, text overlap, and whether to enhance Chinese titles.

After uploading, files and processing configurations are sent to the backend via a POST request (`requests.post("http://localhost:8000/upload_files")`) to add them to the knowledge base.

### 6. File Deletion:

By selecting documents in the table, users can perform bulk deletion. The selected files are sent to the backend via a POST request to complete the deletion operation (`requests.post("http://localhost:8000/delete_kb_files")`).

### 7. Rebuilding the Vector Store:

Users have the option to rebuild the knowledge base's vector store, which is done by sending an API request (`requests.post(f"http://localhost:8000/rebuild_vector_store")`) to update or reconstruct the vector store.

### 8. Deleting the Entire Knowledge Base:

Users can delete the entire knowledge base after confirming the action. The application sends a request to the backend to delete the knowledge base (`requests.post("http://localhost:8000/delete_kb")`).