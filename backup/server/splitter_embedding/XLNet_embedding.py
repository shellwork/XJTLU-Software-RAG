from transformers import XLNetTokenizer, XLNetModel
import torch
from new_ver.backup.server.splitter_embedding.recursive_splitter import split_chunks

def vectorization():
    chunks = split_chunks()
    vector_list = []
    # 加载 XLNet 模型和分词器
    tokenizer = XLNetTokenizer.from_pretrained("xlnet-base-cased", clean_up_tokenization_spaces=True)
    model = XLNetModel.from_pretrained("xlnet-base-cased")

    for chunk in chunks:
        text = chunk.page_content

        # 将文本转换为 XLNet 输入格式
        inputs = tokenizer(text, return_tensors="pt", max_length=200, truncation=True, padding=True)

        # 获取 XLNet 模型的输出
        with torch.no_grad():
            outputs = model(**inputs)

        # 提取句子表示向量（这里使用的是最后一个隐藏层的平均池化作为向量）
        sentence_vector = outputs.last_hidden_state.mean(dim=1).squeeze(0)

        # 将向量添加到列表中
        vector_list.append(sentence_vector)

    return vector_list

# milvus教程里有这个参数，XLNet默认的维度就768，换其他embedding模型可能会变
XLNet_dim = 768