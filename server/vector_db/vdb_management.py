import os
import chromadb
from langchain_chroma import Chroma
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from configs.know_base_config import default_base
from langchain_openai.embeddings import OpenAIEmbeddings

api_key = os.getenv('API_KEY')
embedding_function = OpenAIEmbeddings(model = 'text-embedding-3-small', api_key = api_key)
persist_directory = './chromadb'
client = chromadb.PersistentClient(path = '')
def get_create_collection():
    collection_name = input('Please input your collection name.')
    new_collection = Chroma(
        client=client,
        collection_name="collection_name",
        embedding_function=embedding_function,
    )
    def add_file():
        # 按理来说这里是先写完text splitter + embedding的def然后在导入进来
        embedding_result = embedding_function.embed_documents('texts')
        new_collection.add(
            texts = [''], # splitter后的结果
            embedding = embedding_result, # embedding后的结果
            ids = []
        )

def delete_collection():
    client.delete_collection('collection_name')