from  server.document_loaders.pdf_txt_loader import *
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import XLNetTokenizer, XLNetModel
import torch

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap = 10,
    length_function = len,
    is_separator_regex = False,
)
# document是一个包含单一document对象的list，chunks是包含多个document对象的list
document = create_document()
chunks = text_splitter.split_documents(document)

def vectorization(chunks):
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

vector_list = vectorization(chunks)
for i in vector_list:
    print(i)