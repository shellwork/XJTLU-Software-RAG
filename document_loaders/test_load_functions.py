from langchain_community.document_loaders import (
    UnstructuredWordDocumentLoader,
    CSVLoader,
    PyPDFLoader,
    TextLoader,
    DirectoryLoader,
)
import os
from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader


# load PDF files from directory
# def load_pdf_from_dir_2(directory_path):
#     data = []
#     for filename in os.listdir(directory_path):
#         if filename.endswith(".pdf"):
#             print(filename)
#             # print the file name
#             loader = PyPDFLoader(f'{directory_path}/{filename}')
#             print(loader)
#             data.append(loader.load())
#     return data


# load PDF files from directory
def load_pdf_from_dir(directory_path):
    loader = PyPDFDirectoryLoader(directory_path)
    data = loader.load()
    return data


# load PDF files from a pdf file
def load_pdf_from_one(filepath):
    data = ''
    if filepath.endswith(".pdf"):
        print(filepath)
        # print the file name
        loader = PyPDFLoader(f'{filepath}')
        print(loader)
        data = loader.load()
    return data


# load Word files(.doc/.docx) from directory
def load_word_from_dir(directory_path):
    data = []
    for filename in os.listdir(directory_path):
        # check if the file is a doc or docx file
        # 检查所有doc以及docx后缀的文件
        if filename.endswith(".doc") or filename.endswith(".docx"):
            # langchain自带功能，加载word文档
            loader = UnstructuredWordDocumentLoader(f'{directory_path}/{filename}')
            data.append(loader.load())
    return data


# load Word files(.doc/.docx) from a filename
def load_word_from_one(filename):
    data = ''
    if filename.endswith(".doc") or filename.endswith(".docx"):
        print(filename)
        # print the file name
        loader = UnstructuredWordDocumentLoader(f'{filename}')
        print(loader)
        data = loader.load()
    return data


# load Text files(.txt) from directory
def load_txt_from_dir(directory_path):
    data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            print(filename)
            loader = TextLoader(f'{directory_path}/{filename}')
            print(loader)
            data.append(loader.load())

    return data


# load Text files(.doc/.docx) from a filename
def load_text_from_one(filename):
    data = ''
    if filename.endswith(".txt"):
        print(filename)
        # print the file name
        loader = TextLoader(f'{filename}')
        print(loader)
        data = loader.load()
    return data


# load CSV files(.txt) from directory
def load_csv_from_dir(directory_path):
    data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            print(filename)
            loader = CSVLoader(f'{directory_path}/{filename}')
            print(loader)
            data.append(loader.load())

    return data


# load CSV files(.doc/.docx) from a filename
def load_csv_from_one(filename):
    data = ''
    if filename.endswith(".csv"):
        print(filename)
        # print the file name
        loader = CSVLoader(f'{filename}')
        print(loader)
        data = loader.load()
    return data


# load all files from directory
# param glob = "**/*.文件后缀"  控制要加载的文件
# param show_progress = true 显示进度条
# param use_multithreading = true 利用多线程
# param loader_cls = CSVLoader  指定加载器 | UnstructuredFileLoader

# def load_all_from_dir(directory_path, glob, show_progress=False, use_multithreading=False,
#                       loader_cls=UnstructuredFileLoader):
#     loader = DirectoryLoader(directory_path, glob=glob, show_progress=show_progress,
#                              use_multithreading=use_multithreading, loader_cls=loader_cls)
#     data = loader.load()
#     return data
def load_all_from_dir(directory_path, glob, show_progress=False, use_multithreading=False, loader_cls=UnstructuredFileLoader):
    loader = DirectoryLoader(directory_path, glob=glob, show_progress=show_progress, use_multithreading=use_multithreading, loader_cls=loader_cls)
    data = loader.load()
    return data
def test_load_functions():
    test_directory = "./testdir"
    test_files = {
        "pdf": "sample.pdf",
        "word": "sample.docx",
        "text": "parts key words.txt",
        "csv": ".csv"
    }

    # Test loading PDF files from directory
    print("Testing load_pdf_from_dir")
    pdf_data = load_pdf_from_dir(test_directory)
    print(f"PDF Data: {pdf_data}\n")

    # Test loading a single PDF file
    print("Testing load_pdf_from_one")
    pdf_single_data = load_pdf_from_one(os.path.join(test_directory, test_files["pdf"]))
    print(f"Single PDF Data: {pdf_single_data}\n")

    # Test loading Word files from directory
    print("Testing load_word_from_dir")
    word_data = load_word_from_dir(test_directory)
    print(f"Word Data: {word_data}\n")

    # Test loading a single Word file
    print("Testing load_word_from_one")
    word_single_data = load_word_from_one(os.path.join(test_directory, test_files["word"]))
    print(f"Single Word Data: {word_single_data}\n")

    # Test loading Text files from directory
    print("Testing load_txt_from_dir")
    text_data = load_txt_from_dir(test_directory)
    print(f"Text Data: {text_data}\n")

    # Test loading a single Text file
    print("Testing load_text_from_one")
    text_single_data = load_text_from_one(os.path.join(test_directory, test_files["text"]))
    print(f"Single Text Data: {text_single_data}\n")

    # Test loading CSV files from directory
    print("Testing load_csv_from_dir")
    csv_data = load_csv_from_dir(test_directory)
    print(f"CSV Data: {csv_data}\n")

    # Test loading a single CSV file
    print("Testing load_csv_from_one")
    csv_single_data = load_csv_from_one(os.path.join(test_directory, test_files["csv"]))
    print(f"Single CSV Data: {csv_single_data}\n")

    # Test loading all files from directory
    print("Testing load_all_from_dir")
    all_data = load_all_from_dir(test_directory, "**/*.*")
    print(f"All Data: {all_data}\n")


if __name__ == '__main__':
    test_load_functions()
