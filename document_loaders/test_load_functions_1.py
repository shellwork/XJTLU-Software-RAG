from langchain_community.document_loaders import (
    UnstructuredWordDocumentLoader,
    CSVLoader,
    PyPDFLoader,
    TextLoader,
)

import os

# Load PDF file from a single file
def load_pdf_from_one(filepath):
    if filepath.endswith(".pdf"):
        print(f"Loading PDF file from: {filepath}")
        loader = PyPDFLoader(filepath)
        data = loader.load()
        return data
    return None

# Load Word file (.doc/.docx) from a single file
def load_word_from_one(filepath):
    if filepath.endswith(".doc") or filepath.endswith(".docx"):
        print(f"Loading Word file from: {filepath}")
        loader = UnstructuredWordDocumentLoader(filepath)
        data = loader.load()
        return data
    return None

# Load Text file (.txt) from a single file
def load_text_from_one(filepath):
    if filepath.endswith(".txt"):
        print(f"Loading Text file from: {filepath}")
        loader = TextLoader(filepath)
        data = loader.load()
        return data
    return None

# Load CSV file (.csv) from a single file
def load_csv_from_one(filepath):
    if filepath.endswith(".csv"):
        print(f"Loading CSV file from: {filepath}")
        loader = CSVLoader(filepath)
        data = loader.load()
        return data
    return None

# Test functions
def test_load_functions():
    test_files = {
        "pdf": "E:/Z/XJTLU/iGEM/Chatparts/XJTLU-Software-RAG/document_loaders/testdir/sample.pdf",
        "word": "E:/Z/XJTLU/iGEM/Chatparts/XJTLU-Software-RAG/document_loaders/testdir/sample.docx",
        "text": "E:/Z/XJTLU/iGEM/Chatparts/XJTLU-Software-RAG/document_loaders/testdir/parts key words.txt",
        "csv": "E:/Z/XJTLU/iGEM/Chatparts/XJTLU-Software-RAG/document_loaders/testdir/sample.csv"
    }

    # Test loading a single PDF file
    print("Testing load_pdf_from_one")
    pdf_single_data = load_pdf_from_one(test_files["pdf"])
    print(f"Single PDF Data: {pdf_single_data}\n")

    # Test loading a single Word file
    print("Testing load_word_from_one")
    word_single_data = load_word_from_one(test_files["word"])
    print(f"Single Word Data: {word_single_data}\n")

    # Test loading a single Text file
    print("Testing load_text_from_one")
    text_single_data = load_text_from_one(test_files["text"])
    print(f"Single Text Data: {text_single_data}\n")

    # Test loading a single CSV file
    print("Testing load_csv_from_one")
    csv_single_data = load_csv_from_one(test_files["csv"])
    print(f"Single CSV Data: {csv_single_data}\n")

if __name__ == '__main__':
    test_load_functions()
