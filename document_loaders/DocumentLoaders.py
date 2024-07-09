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


if __name__ == '__main__':
    res = load_pdf_from_dir("./testdir")
    print(res)
