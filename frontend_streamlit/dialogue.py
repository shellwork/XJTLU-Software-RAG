import streamlit as st
import streamlit_antd_components as sac
from streamlit_chatbox import ChatBox
import requests
import uuid
from streamlit_extras.bottom_container import bottom
import os
import sys
from urllib.parse import quote_plus  # Used for URL encoding
from pathlib import Path
sys.path.append("..")
from config import CHATICONS, LOCAL_MODEL_DIR

# Initialize ChatBox
chat_box = ChatBox(assistant_avatar="frontend_streamlit/img/icon.png",
                   user_avatar="frontend_streamlit/img/user.png")  # Replace with your avatar path


# Get local models
def get_local_models():
    """
    Get the list of local models, assuming all local model folders are stored in the 'local_models/' directory
    """
    local_models_dir = os.path.join(LOCAL_MODEL_DIR, "chat")  # Assuming the local model storage path
    if os.path.exists(local_models_dir):
        local_models = [f.name for f in os.scandir(local_models_dir) if f.is_dir()]
    else:
        local_models = []

    local_eb_models_dir = os.path.join(LOCAL_MODEL_DIR, "/embedding")  # Assuming the local model storage path
    if os.path.exists(local_eb_models_dir):
        local_eb_models = [f.name for f in os.scandir(local_models_dir) if f.is_dir()]
    else:
        local_eb_models = []

    return {
        "local_models": local_models,
        "local_eb_models": local_eb_models
    }


# Get API models -> The functionality to fetch API-configured models is not implemented yet, so the names are set directly, and the corresponding model capabilities can be invoked by passing the name
def get_api_models(provider):
    """
    Get the list of available API models
    """
    if provider == "openai":
        local_models = ["gpt-3.5-turbo", "gpt-4"]
        local_eb_models = [
            "default-embedding-model",
        ]
    elif provider == "qwen":
        local_models = ["qwen-long","qwen-plus"]
        local_eb_models = [
            "text-embedding-v1",
            # "text-embedding-async-v1",
            "text-embedding-v2",
            # "text-embedding-async-v2",
            # "text-embedding-v3"
        ]
    else:
        local_models = []
        local_eb_models = []
    return {
        "local_models": local_models,
        "local_eb_models": local_eb_models
    }


# Save and restore session state
def save_session(conv_name: str = None):
    chat_box.context_from_session(
        conv_name, exclude=["selected_page", "prompt", "cur_conv_name", "upload_image"]
    )


def restore_session(conv_name: str = None):
    chat_box.context_to_session(
        conv_name, exclude=["selected_page", "prompt", "cur_conv_name", "upload_image"]
    )


def rerun():
    save_session()
    st.rerun()


# Call the backend API
def call_backend(prompt, tools=None, model="default", eb_models="default", provider="default", use_self_model=False, use_local_model=False):
    try:
        response = requests.post(
            "http://localhost:8000/api/chat",  # Replace with the backend API path
            json={
                "prompt": prompt,
                "tools": tools,
                "model": model,
                "eb_models": eb_models,
                "provider": provider,
                "use_self_model": use_self_model,
                "use_local_model": use_local_model
            }
        )
        response.raise_for_status()  # Check if the request was successful
        data = response.json()  # Parse JSON response
        return data  # Return the entire response
    except requests.RequestException as e:
        st.error(f"Error occurred while requesting backend service: {e}")
        return {"error": "Error occurred while requesting backend service."}


# Export conversation history as a txt file
def export_conversation():
    """
    Export the conversation history of the current session as a txt file
    """
    conv_name = st.session_state.get("cur_conv_name", "Conversation")
    conv_history = get_conversation_history(conv_name)

    if not conv_history:
        st.warning("No conversation history in the current session.")
        return

    # Build conversation content
    content = f"Conversation Name: {conv_name}\n\n"
    for entry in conv_history:
        role = "User" if entry["role"] == "user" else "AI"
        content += f"{role}: {entry['message']}\n"

    # Provide download button
    st.download_button(
        label="Export Conversation History",
        data=content,
        file_name=f"{conv_name}.txt",
        mime="text/plain"
    )


# Get conversation history
def get_conversation_history(conv_name):
    """
    Get the conversation history of the current session
    """
    # Use Streamlit's session_state to store conversation history
    if 'conversations' not in st.session_state:
        st.session_state['conversations'] = {}

    return st.session_state['conversations'].get(conv_name, [])


# Update conversation history
def update_conversation_history(conv_name, role, message):
    """
    Update the conversation history of the current session
    """
    if 'conversations' not in st.session_state:
        st.session_state['conversations'] = {}
    if conv_name not in st.session_state['conversations']:
        st.session_state['conversations'][conv_name] = []
    st.session_state['conversations'][conv_name].append({"role": role, "message": message})


# Define the UI layout for the dialogue page
def dialogue_page():
    ctx = chat_box.context
    ctx.setdefault("uid", uuid.uuid4().hex)
    st.session_state.setdefault("cur_conv_name", chat_box.cur_chat_name)
    st.session_state.setdefault("last_conv_name", chat_box.cur_chat_name)

    if st.session_state.cur_conv_name != st.session_state.last_conv_name:
        save_session(st.session_state.last_conv_name)
        restore_session(st.session_state.cur_conv_name)
        st.session_state.last_conv_name = st.session_state.cur_conv_name

    # Sidebar settings
    with st.sidebar:
        tab2, tab1 = st.tabs(["Conversation", "Settings"])

        with tab1:
            # Enable local model checkbox
            use_local_model = st.checkbox("Enable Local Model", help="Use local model for inference when enabled",
                                          key="use_local_model")
            use_self_model = st.checkbox("Enable Model Dialogue",
                                         help="Use the model's own dialogue capabilities when enabled",
                                         key="use_self_model")

            # Dynamically display available models based on whether the local model is enabled
            if use_local_model:
                available_models = get_local_models().get("local_models")
                model_type = "Local Model"
            else:
                provider = ["openai", "qwen"]
                provider = st.selectbox("Seclect model provider", provider, key="provider")
                available_models = get_api_models(provider).get("local_models")
                model_type = "API Model"

            # Model selection dropdown
            st.selectbox(f"Select {model_type}", available_models, key="selected_model")

            if use_local_model:
                available_eb_models = get_local_models().get("local_eb_models")
                eb_model_type = "Local Embedding Model"
            else:
                available_eb_models = get_api_models(provider).get("local_eb_models")
                eb_model_type = "API Embedding Model"

            # Embedding Model selection dropdown
            st.selectbox(f"Select {eb_model_type}", available_eb_models, key="selected_eb_models")

            # Tool selection
            # tools = st.multiselect("Select Tools", ["Tool1", "Tool2", "Tool3"], key="selected_tools")

        with tab2:
            # Display conversation creation and deletion
            st.write("Conversation Management")

            cols = st.columns(2)
            with cols[0]:
                if st.button("Create New Conversation"):
                    add_conv()

            with cols[1]:
                if st.button("Delete Conversation"):
                    delete_conv()

            conv_names = chat_box.get_chat_names()

            # Display buttons for each conversation
            conversation_name = sac.buttons(
                conv_names,
                label="Current Conversation:",
                key="cur_conv_name",
            )
            chat_box.use_chat_name(conversation_name)

            # Add export button at the bottom of the conversation list
            st.markdown("---")
            export_conversation()

    # Display chat history
    chat_box.output_messages()

    # Input area
    chat_input_placeholder = "Please enter conversation content. Use Shift+Enter for a new line."
    with bottom():
        cols = st.columns([1, 0.2, 15, 1])
        if cols[-1].button(":wastebasket:", help="Clear Conversation"):
            clear_conversation()
            rerun()

        # User input text box
        prompt = cols[2].chat_input(chat_input_placeholder, key="prompt")

    # Process user input
    if prompt and prompt.strip():  # Check if the input is not empty
        chat_box.user_say(prompt.strip())  # Remove leading/trailing whitespace
        update_conversation_history(st.session_state.cur_conv_name, "user",
                                    prompt.strip())  # Update conversation history

        # Call the backend API to get AI response
        ai_response = call_backend(
            prompt.strip(),
            tools=st.session_state.get("selected_tools", []),
            model=st.session_state.get("selected_model"),
            eb_models=st.session_state.get("selected_eb_models"),
            provider=st.session_state.get("provider"),
            use_self_model=st.session_state.get("use_self_model"),
            use_local_model=st.session_state.get("use_local_model")
        )

        # Display response based on mode
        if not st.session_state.get("use_self_model"):
            # Retrieval mode
            chunks = ai_response.get("chunks", [])
            references = ai_response.get("references", [])

            if chunks:
                for idx, (chunk, ref) in enumerate(zip(chunks, references)):
                    with st.expander(f"Related Content {idx + 1}"):
                        st.write(chunk)
                        if ref and ref != "Unknown":
                            # Ensure the path is URL encoded
                            encoded_ref = quote_plus(ref)
                            document_url = f"http://localhost:8000/api/document?source={encoded_ref}"
                            st.markdown(
                                f'<a href="{document_url}" target="_blank">View Referenced Document: {Path(ref).name}</a>',
                                unsafe_allow_html=True)
                            update_conversation_history(st.session_state.cur_conv_name, "ai",
                                                        f"View Referenced Document: {Path(ref).name}")
            else:
                chat_box.ai_say("Could not find enough relevant results, please try a different question.")
                update_conversation_history(st.session_state.cur_conv_name, "ai",
                                            "Could not find enough relevant results, please try a different question.")
        else:
            # Dialogue mode
            answer = ai_response.get("answer", "AI failed to generate a response.")
            references = ai_response.get("references", [])

            chat_box.ai_say(answer)
            update_conversation_history(st.session_state.cur_conv_name, "ai", answer)

            if references:
                st.markdown("**Information Sources:**")
                for ref in references:
                    # Use Markdown hyperlink to trigger document preview
                    encoded_ref = quote_plus(ref)  # URL encode
                    document_url = f"http://localhost:8000/api/document?source={encoded_ref}"
                    st.markdown(f'<a href="{document_url}" target="_blank">Referenced Document: {Path(ref).name}</a>',
                                unsafe_allow_html=True)
                    update_conversation_history(st.session_state.cur_conv_name, "ai",
                                                f"Referenced Document: {Path(ref).name}")


def clear_conversation():
    """
    Clear the conversation history of the current session
    """
    if 'conversations' in st.session_state:
        st.session_state['conversations'][st.session_state.cur_conv_name] = []
    chat_box.reset_history()


# Conversation management function: Add new conversation
def add_conv():
    conv_names = chat_box.get_chat_names()
    i = len(conv_names) + 1
    new_conv_name = f"Conversation{i}"

    # Avoid duplicate conversation names
    while new_conv_name in conv_names:
        i += 1
        new_conv_name = f"Conversation{i}"

    # Update current conversation name
    st.session_state.cur_conv_name = new_conv_name
    chat_box.use_chat_name(new_conv_name)

    # Initialize conversation history
    if 'conversations' not in st.session_state:
        st.session_state['conversations'] = {}
    st.session_state['conversations'][new_conv_name] = []

    # Rerun to update the page display
    rerun()


# Conversation management function: Delete conversation
def delete_conv():
    conv_name_to_delete = st.session_state.cur_conv_name
    conv_names = chat_box.get_chat_names()

    if len(conv_names) > 1:  # Ensure at least one conversation remains
        chat_box.del_chat_name(conv_name_to_delete)

        # Delete conversation history
        if 'conversations' in st.session_state:
            del st.session_state['conversations'][conv_name_to_delete]

        # Switch to another conversation
        st.session_state.cur_conv_name = conv_names[0] if conv_name_to_delete == conv_names[-1] else conv_names[-1]

        # Rerun to update the page display
        rerun()
    else:
        st.warning("At least one conversation must be retained!")


# Main function
if __name__ == "__main__":
    st.set_page_config(
        page_title="Dialogue Interface",
        layout="wide",
    )
    st.title("Multi-functional Dialogue System")
    dialogue_page()
