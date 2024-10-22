import{_ as a,c as t,a0 as s,o as i}from"./chunks/framework.DgZgdyI2.js";const h=JSON.parse('{"title":"🌟 XJTLU-Software iGEM Team Project 2024 🌟","description":"","frontmatter":{},"headers":[],"relativePath":"README.md","filePath":"README.md"}'),n={name:"README.md"};function o(r,e,l,p,d,c){return i(),t("div",null,e[0]||(e[0]=[s(`<h1 id="🌟-xjtlu-software-igem-team-project-2024-🌟" tabindex="-1">🌟 XJTLU-Software iGEM Team Project 2024 🌟 <a class="header-anchor" href="#🌟-xjtlu-software-igem-team-project-2024-🌟" aria-label="Permalink to &quot;🌟 XJTLU-Software iGEM Team Project 2024 🌟&quot;">​</a></h1><p>Welcome to the <strong>XJTLU-Software iGEM Team&#39;s 2024 project</strong> repository! This project is the open source version of <a href="https://gitlab.igem.org/2024/xjtlu-software/software" target="_blank" rel="noreferrer">iGEM competition gitlab repository</a> where we leverage cutting-edge AI and synthetic biology to create innovative tools for biological data management and analysis. <a href="http://2024.igem.wiki/xjtlu-software" target="_blank" rel="noreferrer">More information</a></p><hr><h2 id="📖-project-overview" tabindex="-1">📖 <strong>Project Overview</strong> <a class="header-anchor" href="#📖-project-overview" aria-label="Permalink to &quot;📖 **Project Overview**&quot;">​</a></h2><p>Our project focuses on <strong>enhancing data organization and retrieval</strong> from the iGEM registry by creating a <strong>knowledge base system</strong> that simplifies the process of managing biological components (BioBricks), retrieving experimental data, and enabling efficient querying. The main goals are:</p><ol><li><strong>Centralized Data Management</strong>: Organize biological data into a structured knowledge base.</li><li><strong>Efficient Information Retrieval</strong>: Implement a system for rapid, targeted searches.</li><li><strong>Data Augmentation</strong>: Use AI-driven tools to process and classify biological parts for easier accessibility and utility.</li><li><strong>RAG-based System</strong>: Integrate a <strong>Retrieval-Augmented Generation (RAG)</strong> system to enhance the querying and information management experience.</li></ol><hr><h2 id="🚀-project-purpose" tabindex="-1">🚀 <strong>Project Purpose</strong> <a class="header-anchor" href="#🚀-project-purpose" aria-label="Permalink to &quot;🚀 **Project Purpose**&quot;">​</a></h2><p>The primary aim is to <strong>solve the inefficiencies</strong> in the current iGEM parts registry by offering:</p><ul><li>A structured <strong>knowledge base</strong> where raw experimental data can be organized, categorized, and retrieved efficiently.</li><li>A user-friendly interface for <strong>uploading, managing, and querying biological data</strong>.</li><li><strong>AI-enhanced</strong> tools for handling large-scale biological datasets, allowing for precise and rapid retrieval of information.</li></ul><hr><h2 id="🗂️-project-file-structure-–-xjtlu-software-igem-team-2024" tabindex="-1">🗂️ <strong>Project File Structure</strong> – <em>XJTLU-Software iGEM Team 2024</em> <a class="header-anchor" href="#🗂️-project-file-structure-–-xjtlu-software-igem-team-2024" aria-label="Permalink to &quot;🗂️ **Project File Structure** – *XJTLU-Software iGEM Team 2024*&quot;">​</a></h2><p>This repository contains the essential components of the <strong>XJTLU-Software iGEM Team&#39;s 2024 project</strong>. Below is a description of the most relevant files and directories in the project:</p><div class="language- vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang"></span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>├── backup/                     # Folder for storing backups of previous work</span></span>
<span class="line"><span>├── data/                       # Contains the data uploaded to the system (Knowledge Base storage)</span></span>
<span class="line"><span>│   ├── uploads/                # Subfolder where uploaded files are categorized and saved</span></span>
<span class="line"><span>├── docs/                       # Documentation for the project</span></span>
<span class="line"><span>├── frontend_streamlit/          # Streamlit front-end for user interactions with the knowledge base</span></span>
<span class="line"><span>│   ├── knowledge_base.py       # Main front-end script for managing the knowledge base via UI</span></span>
<span class="line"><span>├── knowledge_base/              # Logic and functionality for knowledge base operations</span></span>
<span class="line"><span>├── server/                      # Backend server code for managing the knowledge base</span></span>
<span class="line"><span>│   ├── api.py                  # API routes for handling file uploads, deletions, and vector store operations</span></span>
<span class="line"><span>│   ├── data_loader/            # Logic for loading data from various file formats</span></span>
<span class="line"><span>│   ├── model/                  # Model selection and embedding functionality</span></span>
<span class="line"><span>│   └── chroma_utils.py         # Utilities for Chroma vector store operations</span></span>
<span class="line"><span>├── config.py                    # Centralized configuration file for paths and settings</span></span>
<span class="line"><span>├── LICENSE                      # License information for the project</span></span>
<span class="line"><span>├── README.md                    # Detailed project documentation</span></span>
<span class="line"><span>├── requirements.txt             # Python dependencies for setting up the environment</span></span>
<span class="line"><span>├── setup.py                     # Script for setting up the package</span></span>
<span class="line"><span>└── webui.py                     # Main entry point for launching the UI interface via Streamlit</span></span></code></pre></div><h3 id="key-folders-and-files" tabindex="-1">Key Folders and Files: <a class="header-anchor" href="#key-folders-and-files" aria-label="Permalink to &quot;Key Folders and Files:&quot;">​</a></h3><ul><li><p><strong>backup/</strong>: Contains backups of critical files or versions of the project.</p></li><li><p><strong>data/</strong>: The main storage for uploaded documents, organized into subfolders based on categories (file types).</p><ul><li><strong>uploads/</strong>: Subfolder where files uploaded via the knowledge base UI are stored.</li></ul></li><li><p><strong>docs/</strong>: Project documentation such as technical guides, API references, and usage instructions.</p></li><li><p><strong>frontend_streamlit/</strong>: Contains the front-end logic using Streamlit for providing an interactive UI for knowledge base management.</p><ul><li><strong>knowledge_base.py</strong>: The primary file responsible for user interaction with the knowledge base, including file uploads, deletions, and querying.</li></ul></li><li><p><strong>knowledge_base/</strong>: This folder holds the backend logic related to knowledge base operations such as file management, categorization, and vectorization.</p></li><li><p><strong>server/</strong>: Backend logic that powers the project, including data loaders, model selectors, and API endpoints.</p><ul><li><strong>api.py</strong>: Exposes endpoints for interacting with the knowledge base.</li><li><strong>data_loader/</strong>: Contains the logic to handle various types of files, including documents and OCR files.</li><li><strong>model/</strong>: Includes tools for selecting and using embedding models for processing data.</li><li><strong>chroma_utils.py</strong>: Manages Chroma vector store operations such as updating and rebuilding the vector store.</li></ul></li><li><p><strong>config.py</strong>: Stores global configurations such as file paths (<code>DATA_PATH</code>, <code>CHROMA_PATH</code>) to streamline adjustments and ensure consistency across the project.</p></li><li><p><strong>webui.py</strong>: The main Streamlit UI application that acts as the interface for the knowledge base, allowing users to interact with the system through a browser.</p></li></ul><hr><h2 id="🛠️-features-and-functionality" tabindex="-1">🛠️ <strong>Features and Functionality</strong> <a class="header-anchor" href="#🛠️-features-and-functionality" aria-label="Permalink to &quot;🛠️ **Features and Functionality**&quot;">​</a></h2><ul><li><p><strong>Knowledge Base Management</strong>:</p><ul><li>Create, delete, and manage knowledge bases using a structured folder system.</li><li>Files are automatically categorized based on their extensions into appropriate folders.</li></ul></li><li><p><strong>File Upload and Categorization</strong>:</p><ul><li>Users can upload files directly via the Streamlit interface, and the files are automatically categorized and stored based on their file type.</li></ul></li><li><p><strong>Chroma Vector Store Integration</strong>:</p><ul><li>Use Chroma for vectorization of document chunks, enabling efficient information retrieval using embeddings.</li></ul></li><li><p><strong>Dynamic Query and Update</strong>:</p><ul><li>The system allows users to upload and delete files, rebuild vector stores, and query the knowledge base through a streamlined interface.</li></ul></li></ul><hr><h2 id="💻-technology-stack" tabindex="-1">💻 <strong>Technology Stack</strong> <a class="header-anchor" href="#💻-technology-stack" aria-label="Permalink to &quot;💻 **Technology Stack**&quot;">​</a></h2><ul><li><p><strong>Backend</strong>:</p><ul><li><strong>FastAPI</strong>: Provides a fast, efficient API for handling knowledge base operations.</li><li><strong>Chroma</strong>: Used as the vector store for managing embeddings and retrieval.</li><li><strong>LangChain</strong>: For document chunking and handling large documents.</li><li><strong>Python</strong>: The main programming language for building APIs, data processing, and AI integration.</li></ul></li><li><p><strong>Frontend</strong>:</p><ul><li><strong>Streamlit</strong>: Offers an interactive, easy-to-use front-end interface for managing knowledge bases and interacting with the system.</li><li><strong>VuePress</strong>: A minimalistic static site generator built on Vue, perfect for creating elegant documentation sites with ease.</li></ul></li></ul><hr><h2 id="⚙️-setup-and-installation" tabindex="-1">⚙️ <strong>Setup and Installation</strong> <a class="header-anchor" href="#⚙️-setup-and-installation" aria-label="Permalink to &quot;⚙️ **Setup and Installation**&quot;">​</a></h2><ol><li><p>Clone the repository:</p><div class="language-bash vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">bash</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">git</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> clone</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> https://github.com/XJTLU-Software-iGEM/2024-project.git</span></span>
<span class="line"><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">cd</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> 2024-project</span></span></code></pre></div></li><li><p>Install the required dependencies:</p><div class="language-bash vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">bash</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">pip</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> install</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> -r</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> requirements.txt</span></span></code></pre></div></li><li><p>create <code>.env</code> files in the root folder and update your api keys</p><div class="language-bash vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">bash</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">OPENAI_API_KEY</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;your api key&quot;</span></span></code></pre></div></li><li><p>Run setup.py to open ChatParts</p><div class="language-bash vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">bash</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">python</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> setup.py</span></span></code></pre></div></li></ol><p>or try to run following process below</p><ol start="4"><li><p>Run the backend API:</p><div class="language-bash vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">bash</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">uvicorn</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> server.api:app</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> --reload</span></span></code></pre></div></li><li><p>Run the frontend (Streamlit):</p><div class="language-bash vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">bash</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">streamlit</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> run</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> frontend_streamlit/knowledge_base.py</span></span></code></pre></div></li></ol><hr><h2 id="🤝-contributing" tabindex="-1">🤝 <strong>Contributing</strong> <a class="header-anchor" href="#🤝-contributing" aria-label="Permalink to &quot;🤝 **Contributing**&quot;">​</a></h2><p>We welcome contributions! If you have any suggestions or improvements, feel free to fork the repo and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.</p><hr><h2 id="🔗-links" tabindex="-1">🔗 <strong>Links</strong> <a class="header-anchor" href="#🔗-links" aria-label="Permalink to &quot;🔗 **Links**&quot;">​</a></h2><ul><li>Official Website: <a href="https://www.xjtlu.edu.cn/zh/igem" target="_blank" rel="noreferrer">XJTLU iGEM</a></li><li>Project Documentation: <a href="https://your_project_docs_link" target="_blank" rel="noreferrer">Docs(comming soon)</a></li><li>Original Respository: <a href="https://gitlab.igem.org/2024/xjtlu-software/software" target="_blank" rel="noreferrer">iGEM Gitlab</a></li><li>Team Wiki: <a href="http://2024.igem.wiki/xjtlu-software" target="_blank" rel="noreferrer">XJTLU-Software 2024</a></li></ul><hr><h3 id="🏅-acknowledgments" tabindex="-1">🏅 <strong>Acknowledgments</strong> <a class="header-anchor" href="#🏅-acknowledgments" aria-label="Permalink to &quot;🏅 **Acknowledgments**&quot;">​</a></h3><p>This project is a collaborative effort of the <strong>XJTLU-Software iGEM Team</strong>. Special thanks to all team members for their contributions and dedication to the project.</p><h3 id="🙏-special-thanks" tabindex="-1">🙏 <strong>Special Thanks</strong> <a class="header-anchor" href="#🙏-special-thanks" aria-label="Permalink to &quot;🙏 **Special Thanks**&quot;">​</a></h3><p>This project was inspired by some incredible open-source contributions and tools. We would like to extend our heartfelt gratitude to the following:</p><ul><li><p>Langchain-Chatchat: This project served as the inspiration for our work, and we are deeply grateful to the creators for their innovative contributions.</p></li><li><p>iGEM Wiki Theme: A special thanks to the author of the <a href="https://gitlab.igem.org/2022/epfl" target="_blank" rel="noreferrer">EPFL iGEM wiki</a> theme for providing a beautifully crafted template that helped guide the structure of our project&#39;s documentation and presentation.</p></li></ul><p>These projects have specially inspired our work, and we are incredibly grateful for their creators&#39; dedication to the open-source community.</p><hr><p><strong>Made with ❤️ by the XJTLU-Software iGEM Team</strong></p><hr>`,43)]))}const u=a(n,[["render",o]]);export{h as __pageData,u as default};