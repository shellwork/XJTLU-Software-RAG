# Frontend of Chat system

We created a multi-functional chat system using Streamlit. It features a user interface for managing conversations, enabling users to upload files, interact with AI models, and view historical chat data. Key functions include selecting between local and API models, saving and restoring session states, calling a backend API for responses, and exporting conversation logs. Users can create, delete, and switch between conversations while tracking the chat history. The chat interactions are facilitated through a ChatBox component, and the system is designed to handle various configurations and options for personalized user experience.

## Components and functionalities:

### Imports and Initialization:

The code imports necessary libraries, including Streamlit and components for chat interaction.
A `ChatBox` is initialized to manage the chat interface.

### Model Management:

Functions `get_local_models()` and `get_api_models()` retrieve lists of local and API-based AI models for users to choose from.

### Session Management:

Functions `save_session()` and `restore_session()` handle saving and restoring the chat context to maintain conversation history across interactions.

### API Interaction:

The `call_backend()` function sends user prompts to a backend API and returns the AI's response, handling errors as necessary.

### Conversation History Management:

Functions `get_conversation_history()` and `update_conversation_history()` manage and store the dialogue history using Streamlit's session state.

### User Interface:

The `dialogue_page()` function defines the layout of the chat interface, including sidebar settings for model selection and conversation management.

Users can create or delete conversations and view or export chat histories.

### Chat Interaction:

Users can input messages, and the AI's responses are processed and displayed, with options for using either local models or API models.

The interface supports exporting conversations as text files.

### Clear Conversations:

A function `clear_conversation()` allows users to reset the current chat history.

### Session Control:

Functions `add_conv()` and `delete_conv()` manage the creation and deletion of chat sessions, ensuring at least one session is retained.
