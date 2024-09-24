# Special Document Loader
<br/>

The **`load_text_documents`** function is designed to load PDF documents and extract text from them based on a specified list of files.

**Input parameters:**

`kb_name`: The name of the knowledge base, which specifies the directory containing the PDF files.

`files`: A list of filenames to be processed.

**Return value:**

Returns a list of `Document` objects containing the extracted text.

```python
def load_text_documents(kb_name: str, files: list[str]) -> list[Document]:
    """
    Loads a PDF document extracted by text, processing only the specified file based on the list of files passed in.

    :param kb_name: name of knowledge base
    :param files: file list to be processed
    :return: Document object list
    """
    base_path = Path(DATA_PATH) / kb_name
    file_set = set(files)  # Converts a list of incoming files into a set for quick lookups
    text_documents = []
    # Collect the path of the PDF file to be processed
    pdf_paths = [str(pdf_file) for pdf_file in base_path.rglob("*.pdf") if pdf_file.name in file_set]
    if not pdf_paths:
        return text_documents

    # Use concurrent loader to process PDF files
    loader = PDFTextLoader(pdf_paths=pdf_paths)
    text_documents.extend(loader.load())

    return text_documents

```

<br/>

---
The **`load_ocr_documents`** function is designed to load and process image files using Optical Character Recognition (OCR).

```python
def load_ocr_documents(kb_name: str, files: list[str]) -> list[Document]:
    """
    Loads OCR documents and process only image files.

    :param kb_name: name of knowledge base
    :param files: file list to be processed
    :return: Document object list
    """
    base_path = Path(kb_name)
    file_set = set(files)  # Converts a list of incoming files into a set for quick lookups

    # Load image file and OCR processing
    image_documents = []
    for img_file in base_path.rglob("*.png"):
        if img_file.name in file_set:  # Only process the files in the incoming file list
            img_loader = DirectoryLoader(str(img_file.parent), loader_cls=RapidOCRLoader, glob=img_file.name)
            image_documents.extend(img_loader.load())

    # Combine with OCR processing of the picture document
    documents = image_documents
    return documents
```

<br/>

---
The **`load_documents_combined`** function is designed to load and combine documents from different sources.

```python
def load_documents_combined(kb_name: str, files: list[str]) -> list[Document]:
    """
    Load all documents, including text extracted PDF and OCR processed images.

    :param kb_name: name of knowledge base
    :param files: file list to be processed
    :return: Document object list
    """
    text_docs = load_text_documents(kb_name, files)
    ocr_docs = load_ocr_documents(kb_name, files)
    combined_docs = text_docs + ocr_docs
    return combined_docs
```