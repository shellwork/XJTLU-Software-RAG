
# 🌟 XJTLU-Software iGEM Team Project 2024 🌟

Welcome to the **XJTLU-Software iGEM Team's 2024 project** repository! This project is the open source version of [iGEM competition gitlab repository](https://gitlab.igem.org/2024/xjtlu-software/software) where we leverage cutting-edge AI and synthetic biology to create innovative tools for biological data management and analysis. [More information](http://2024.igem.wiki/xjtlu-software)

---

## 📖 **Project Overview**

Our project focuses on **enhancing data organization and retrieval** from the iGEM registry by creating a **knowledge base system** that simplifies the process of managing biological components (BioBricks), retrieving experimental data, and enabling efficient querying. The main goals are:

1. **Centralized Data Management**: Organize biological data into a structured knowledge base.
2. **Efficient Information Retrieval**: Implement a system for rapid, targeted searches.
3. **Data Augmentation**: Use AI-driven tools to process and classify biological parts for easier accessibility and utility.
4. **RAG-based System**: Integrate a **Retrieval-Augmented Generation (RAG)** system to enhance the querying and information management experience.

---

## 🚀 **Project Purpose**

The primary aim is to **solve the inefficiencies** in the current iGEM parts registry by offering:
- A structured **knowledge base** where raw experimental data can be organized, categorized, and retrieved efficiently.
- A user-friendly interface for **uploading, managing, and querying biological data**.
- **AI-enhanced** tools for handling large-scale biological datasets, allowing for precise and rapid retrieval of information.

---

## 🗂️ **Project File Structure** – *XJTLU-Software iGEM Team 2024*

This repository contains the essential components of the **XJTLU-Software iGEM Team's 2024 project**. Below is a description of the most relevant files and directories in the project:

```
├── backup/                     # Folder for storing backups of previous work
├── data/                       # Contains the data uploaded to the system (Knowledge Base storage)
│   ├── uploads/                # Subfolder where uploaded files are categorized and saved
├── docs/                       # Documentation for the project
├── frontend_streamlit/          # Streamlit front-end for user interactions with the knowledge base
│   ├── knowledge_base.py       # Main front-end script for managing the knowledge base via UI
├── knowledge_base/              # Logic and functionality for knowledge base operations
├── server/                      # Backend server code for managing the knowledge base
│   ├── api.py                  # API routes for handling file uploads, deletions, and vector store operations
│   ├── data_loader/            # Logic for loading data from various file formats
│   ├── model/                  # Model selection and embedding functionality
│   └── chroma_utils.py         # Utilities for Chroma vector store operations
├── config.py                    # Centralized configuration file for paths and settings
├── LICENSE                      # License information for the project
├── README.md                    # Detailed project documentation
├── requirements.txt             # Python dependencies for setting up the environment
├── setup.py                     # Script for setting up the package
└── webui.py                     # Main entry point for launching the UI interface via Streamlit
```

### Key Folders and Files:

- **backup/**: Contains backups of critical files or versions of the project.
- **data/**: The main storage for uploaded documents, organized into subfolders based on categories (file types).
  - **uploads/**: Subfolder where files uploaded via the knowledge base UI are stored.
  
- **docs/**: Project documentation such as technical guides, API references, and usage instructions.

- **frontend_streamlit/**: Contains the front-end logic using Streamlit for providing an interactive UI for knowledge base management.
  - **knowledge_base.py**: The primary file responsible for user interaction with the knowledge base, including file uploads, deletions, and querying.

- **knowledge_base/**: This folder holds the backend logic related to knowledge base operations such as file management, categorization, and vectorization.

- **server/**: Backend logic that powers the project, including data loaders, model selectors, and API endpoints.
  - **api.py**: Exposes endpoints for interacting with the knowledge base.
  - **data_loader/**: Contains the logic to handle various types of files, including documents and OCR files.
  - **model/**: Includes tools for selecting and using embedding models for processing data.
  - **chroma_utils.py**: Manages Chroma vector store operations such as updating and rebuilding the vector store.

- **config.py**: Stores global configurations such as file paths (`DATA_PATH`, `CHROMA_PATH`) to streamline adjustments and ensure consistency across the project.

- **webui.py**: The main Streamlit UI application that acts as the interface for the knowledge base, allowing users to interact with the system through a browser.

---

## 🛠️ **Features and Functionality**

- **Knowledge Base Management**: 
    - Create, delete, and manage knowledge bases using a structured folder system.
    - Files are automatically categorized based on their extensions into appropriate folders.
  
- **File Upload and Categorization**: 
    - Users can upload files directly via the Streamlit interface, and the files are automatically categorized and stored based on their file type.
  
- **Chroma Vector Store Integration**:
    - Use Chroma for vectorization of document chunks, enabling efficient information retrieval using embeddings.

- **Dynamic Query and Update**:
    - The system allows users to upload and delete files, rebuild vector stores, and query the knowledge base through a streamlined interface.

---

## 💻 **Technology Stack**

- **Backend**:
  - **FastAPI**: Provides a fast, efficient API for handling knowledge base operations.
  - **Chroma**: Used as the vector store for managing embeddings and retrieval.
  - **LangChain**: For document chunking and handling large documents.
  - **Python**: The main programming language for building APIs, data processing, and AI integration.

- **Frontend**:
  - **Streamlit**: Offers an interactive, easy-to-use front-end interface for managing knowledge bases and interacting with the system.
  - **VuePress**: A minimalistic static site generator built on Vue, perfect for creating elegant documentation sites with ease.
---

## ⚙️ **Setup and Installation**

1. Clone the repository:
    ```bash
    git clone https://github.com/XJTLU-Software-iGEM/2024-project.git
    cd 2024-project
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   
3. create `.env` files in the root folder and update your api keys
    ```bash
    OPENAI_API_KEY="your api key"
    ```

4. Run setup.py to open ChatParts
    ```bash
    python setup.py
    ```
   
or try to run following process below

4. Run the backend API:
    ```bash
    uvicorn server.api:app --reload
    ```

5. Run the frontend (Streamlit):
    ```bash
    streamlit run frontend_streamlit/knowledge_base.py
    ```

---

## 🤝 **Contributing**

We welcome contributions! If you have any suggestions or improvements, feel free to fork the repo and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

---

## 🔗 **Links**

- Official Website: [XJTLU iGEM](https://www.xjtlu.edu.cn/zh/igem)
- Project Documentation: [Docs(comming soon)](https://your_project_docs_link)
- Original Respository: [iGEM Gitlab](https://gitlab.igem.org/2024/xjtlu-software/software)
- Team Wiki: [XJTLU-Software 2024](http://2024.igem.wiki/xjtlu-software)

---

### 🏅 **Acknowledgments**

This project is a collaborative effort of the **XJTLU-Software iGEM Team**. Special thanks to all team members for their contributions and dedication to the project.

### 🙏 **Special Thanks**

This project was inspired by some incredible open-source contributions and tools. We would like to extend our heartfelt gratitude to the following:

- Langchain-Chatchat: This project served as the inspiration for our work, and we are deeply grateful to the creators for their innovative contributions.

- iGEM Wiki Theme: A special thanks to the author of the [EPFL iGEM wiki](https://gitlab.igem.org/2022/epfl) theme for providing a beautifully crafted template that helped guide the structure of our project's documentation and presentation.

These projects have specially inspired our work, and we are incredibly grateful for their creators' dedication to the open-source community.

---

**Made with ❤️ by the XJTLU-Software iGEM Team**

--- 
