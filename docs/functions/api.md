# API

The code in the api file is built using the FastAPI framework to create a backend service primarily designed for managing and operating a document-based knowledge base system. It handles file uploads, OCR processing, and various other functionalities.

## Libraries imported

`sys`, `uuid`, `Path`: Used for handling system paths and generating unique batch IDs.

`logging`: Used for recording log information, aiding in debugging and tracking system behavior.

`fastapi` related importers: Used to create API routes and handle HTTP requests.

`tqdm`：To create progress bar prompts.

## Configuration and Initialization

`current_dir` and `project_root`：Retrieve the current file path and the project root directory, add the root directory to the system path to ensure modules can be imported from it.

app.mount("/uploads")：Mounts the `data/uploads` directory as a static file directory, providing direct access to uploaded files.

## API Routes

**· Chat Interface (`/api/chat`):**

Handles chat requests by calling the generate_response function to produce an AI-generated reply.

**· Get Document Interface (`/api/document`):**

Retrieves the content of a specified document based on the `source` parameter (document path). It can return either text files (e.g., `.txt`, `.json`, `.csv`) or image files (e.g., `.png`, `.jpg`), returning either the file content or the file URL, respectively.

**· File Upload Interface (`/upload_files`):**

Allows users to upload files, generating a unique batch ID for each upload. It supports parameters like file chunk size and overlap settings.

Uploaded files are saved to the knowledge base, and the system updates the corresponding metadata for the knowledge base.

**· Create Knowledge Base Interface (`/create_kb`):**

Used to create a new knowledge base, accepting parameters such as the knowledge base name, type, and embedding model.

**· Get Knowledge Base List Interface (`/get_kb_list`):**

Returns a list of all created knowledge bases.

**· Get Documents in Knowledge Base Interface (`/get_kb_documents`):**

Retrieves a list of all documents within a specified knowledge base.

**· Rebuild Vector Store Interface (`/rebuild_vector_store`):**

Reprocesses and vectorizes the documents in a specified knowledge base, with the option to delete the existing vector store and rebuild it.

**· Delete Knowledge Base Interface (`/delete_kb`):**

Deletes the specified knowledge base along with its contents.

**· Delete Files from Knowledge Base Interface (`/delete_kb_files`):**

Deletes specified files from a knowledge base.

