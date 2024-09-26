# Knowledge Base Management

The create-database file is part of a knowledge management system that handles document processing and vector embedding for a knowledge base (KB). It uses the **FastAPI** framework to upload, store, and manage documents in various formats (e.g., PDFs, JSON, OCR documents). The knowledge base can also utilize different vector store backends (e.g., **Chroma**) for information retrieval and is capable of batch processing and metadata management.

## Key Functionalities:

### 1. Initialization Functions:

· `initialize_upload_path()`: Sets up the folder structure for storing uploaded documents.

· `initialize_metadata()`: Initializes metadata (`metadata.json`) for a specific knowledge base if it doesn't exist.

<br/>

### 2. Knowledge Base Management:

· `create_kb()`: Creates a new knowledge base folder, initializes metadata, and configures parameters like embedding model and vector store type.

· `get_kb_list()`: Retrieves a list of available knowledge bases and categorizes their documents.

· `get_kb_documents()`: Returns a list of documents in a specified knowledge base, along with their sizes, chunking settings, and metadata.

· `delete_kb()`: Deletes an entire knowledge base, including its metadata and documents.

<br/>

### 3. Document Management:

· `save_file_to_category()`: Saves uploaded documents into categorized folders within a knowledge base based on file extensions.

· `delete_kb_files()`: Deletes specific files from a knowledge base and updates the metadata accordingly.

<br/>

### 4. Batch Processing:

`process_batches()`: Handles batch processing of documents by splitting, vectorizing, and storing them in the vector store. It also assigns default parameters to files that haven’t been processed in a batch.

<br/>

### 5. Vector Store Operations:

· `generate_data_store()`: This function handles the core document processing workflow, including text splitting, vectorization, and embedding model processing (e.g., using Chroma). It also supports special processing of JSON and OCR documents.

· `delete_existing_chroma()`: Deletes the existing Chroma vector database when needed.

<br/>

### 6. Metadata Handling:

· `read_kb_metadata()`: Reads the metadata file (`metadata.json`) for a specified knowledge base. If it doesn’t exist, it initializes the file.

· `update_kb_metadata()`: Updates metadata, especially for batch-related information.