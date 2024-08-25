from server.splitter_embedding.XLNet_embedding import *
from server.splitter_embedding.recursive_splitter import split_chunks
from pymilvus import MilvusClient
from tqdm import tqdm

# 创建collection
milvus_client = MilvusClient(uri="./hf_milvus_demo.db")
collection_name = 'rag'

# 检查collection是否存在
if milvus_client.has_collection(collection_name):
    milvus_client.drop_collection(collection_name)

milvus_client.create_collection(
    collection_name=collection_name,
    dimension=XLNet_dim,
    metric_type="IP",  # Inner product distance
    consistency_level="Strong",  # Strong consistency level
)

data = []
chunks = split_chunks()
text_lines = [chunks.page_content for chunk in chunks]

# 其他地方都和你发给我的代码一样，只有下面这个vector不一样，它的embed函数返回的list(list),我的vectorization是list(torch.Tensor)
for i, line in enumerate(tqdm(text_lines, desc="Creating embeddings")):
    data.append({"id": i, "vector": vectorization(line), "text": line})

insert_res = milvus_client.insert(collection_name=collection_name, data=data)
insert_res["insert_count"]