import os

default_base = 'knowledge-base-1'

# offline knowledge base service
default_vectorstore_type = 'milvus'
#number of matching vectors
top_k = 4
# matching relevance threshold
score = 0.5
chunk_size = 250
overlap_size = 20

#搜索引擎相关top K和搜索引擎选择，暂时不写

# knowledge base stroage path
kb_root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base")
if not os.path.exists(kb_root_path):
    os.mkdir(kb_root_path)

db_root_path = os.path.join(kb_root_path, "info.db")
sqlalchemy_database_uri = f"sqlite:///{db_root_path}"

# vectorstore config
kb_config = {
    'milvus' : {
        'host' : '127.0.0.1',
        'port' : '19530',
        'user' : '',
        'password': '',
        'secure': False
    },
    'chroma' : {
        'host' : '127.0.0.1',
        'port' : '8000',
        'user' : '',
        'password' : '',
        'secure' : False
    }
}

text_splitter = {
    'RecursiveCharacterTextSplitter' : {
        'source' : 'tiktoken',
        'tokenizer_name_path' : 'cl100k_base'
    }
}

splitter_name = 'RecursiveCharacterTextSplitter'