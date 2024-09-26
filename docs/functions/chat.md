# Question -Answer System

The chat file is based on the LangChain framework, combining vector databases with large language models to build a question-answering system. It can provide retrieval-based answers (RAG, Retrieval-Augmented Generation) or model-generated responses based on the user's input. 

## Key Functionalities:

### 1. Imported Libraries:

· **`Chroma`**: Used for managing a vector database, supporting persistent storage and similarity-based searches.

· **`ChatPromptTemplate`**: Used to create and format dialogue prompt templates.

· **`get_model`** and **`get_embedding_function`**: These functions, from the custom `model_selector` module, are responsible for fetching the model and embedding function.

· **Path** and **sys**: Handle paths to ensure correct import of configurations and modules.

· **`config`**: From the `config` module, imports `RAG_PROMPT_TEMPLATE` and `CHROMA_PATH`, which refer to the dialogue template and the path for vector database storage.

<br/>

### 2. `generate_response` Function: 

This is the core function of the system, generating a response based on user input. It combines vector database search with a language model's generation capabilities.

#### Parameters:

· `prompt`: The user's input question or dialogue.

· `tools`: Optional parameter, used to specify if certain tools are employed (not implemented in the given code).

· `model`: The name of the model to use, defaulting to "default".

· `use_self_model`: Specifies whether to generate responses using a custom model. If False, only retrieval-based document chunks are returned. If `True`, the function combines the language model's generated dialogue.

· `use_local_model`: Specifies whether to use a local model for inference.

<br/>

### 3. Vector Database Query:

· The function first calls `get_embedding_function()` to retrieve the embedding function and uses it along with the `CHROMA_PATH` to initialize a Chroma vector database.

· Through `db.similarity_search_with_relevance_scores(prompt, k=3)`, the database performs a similarity search and returns the document chunks most relevant to the user's input, along with relevance scores.

<br/>

### 4. Two Response Modes:

<br/>

##### Retrieval Mode (`use_self_model=False`): 

If custom model generation is not used, the function returns only the most relevant document chunks and their reference information.

· If the highest similarity score is greater than or equal to 0.7, relevant document chunks and their sources are returned.

· Otherwise, empty document chunks and references are returned.

##### Dialogue Mode (`use_self_model=True`): 

If a custom model is used to generate dialogue, it further combines the retrieved document chunks with the model's generated answer.

· First, it calls `get_model` to fetch the specified model and generates a response from the model.

· If relevant retrieval results exist (score >= 0.7), the document chunks are formatted as context and used along with the model's response to create a final answer using a template.

· If no highly relevant results are found, it returns the model-generated answer directly.

<br/>

### 5. Return Structure:

The function returns a dictionary containing the generated answer (`answer`) or the retrieved document chunks (`chunks`), as well as their reference sources (`references`).