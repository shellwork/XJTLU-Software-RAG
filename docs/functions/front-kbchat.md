# Knowledge Base Chat

This file implements a Retrieval-Augmented Generation (RAG) dialogue system using the Streamlit framework. The system features a chat interface that allows users to interact with various dialogue modes, such as knowledge base Q&A, file conversations, and search engine queries.

## Key components:

### 1. Configuration and Utility Classes:

The `Settings` class holds various configuration parameters for the model and tools, including history length, knowledge base settings, and search engine configurations.

A dummy `ApiRequest` class contains a placeholder for fetching available knowledge bases, with the `list_knowledge_bases()` method set to return a static list.

<br/>

### 2. Chat Interface Setup:

A `ChatBox` instance is initialized to manage the user interface for the chat, complete with an avatar.

The `init_widgets()` function initializes the session state to keep track of user selections and parameters.

<br/>

### 3. User Interaction:

The `kb_chat()` function creates the main UI layout, featuring a sidebar with tabs for RAG configuration and session settings.

Users can select a dialogue mode, configure settings, and upload files as needed. The chat history is displayed, and users can input messages via a chat box, which are echoed back as simulated AI responses.

<br/>

### 4. Export Functionality:

The system includes an option to export the chat history as a markdown file, timestamped for easy identification.