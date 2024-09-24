# Document Loader
<br/>

The **`load_ori_documents`** function is designed to load specific types of documents (`.md`, `.txt`, `.docx`, and `.pptx`) from a specified knowledge base.

**Input parameters:**

· `kb_name`: The path of the knowledge base.

· `files`: The names of the files to be loaded.


**Return value:**
The function returns a list containing all the loaded documents, with the document type being `Document` objects.

<br/>

```python
def load_ori_documents(kb_name: str, files: list[str]) -> list[Document]:
    """
    Load regular documents, processing only the specified files based on the 
    provided file list.
    """
    base_path = Path(kb_name)
    # Converts a list of incoming files into a collection for quick lookups
    file_set = set(files)  

    # Load .md documents
    md_documents = []
    for md_file in base_path.rglob("*.md"):
        # Only process the files in the provided file list
        if md_file.name in file_set:  
            loader = DirectoryLoader(str(md_file.parent), glob=md_file.name)
            md_documents.extend(loader.load())

    # Load .txt documents
    txt_documents = []
    for txt_file in base_path.rglob("*.txt"):
        # Only process the files in the provided file list
        if txt_file.name in file_set:  
            txt_loader = DirectoryLoader(str(txt_file.parent), glob=txt_file.name)
            txt_documents.extend(txt_loader.load())

    # Load .docx documents
    docx_documents = []
    for docx_file in base_path.rglob("*.docx"):
        # Only process the files in the provided file list
        if docx_file.name in file_set:  
            docx_loader = DirectoryLoader(str(docx_file.parent), glob=docx_file.name)
            docx_documents.extend(docx_loader.load())

    # Load .pptx documents
    pptx_documents = []
    for pptx_file in base_path.rglob("*.pptx"):
        # Only process the files in the provided file list
        if pptx_file.name in file_set:  
            pptx_loader = DirectoryLoader(str(pptx_file.parent), glob=pptx_file.name)
            pptx_documents.extend(pptx_loader.load())

    # Combine all non-structured documents
    documents = md_documents + txt_documents + docx_documents + pptx_documents
    return documents
```