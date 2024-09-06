import json
from pathlib import Path
from langchain.schema import Document

def load_json_documents(path: str) -> list[Document]:
    json_documents = []
    base_path = Path(path)  # 使用传入的路径作为基准路径

    # 遍历 data 文件夹下的所有子目录和文件，查找 .json 文件
    for json_file in base_path.rglob("*.json"):  # rglob 递归查找所有 .json 文件
        print(f"Loading JSON document: {json_file}")
        with open(json_file, "r", encoding="utf-8") as file:
            json_data = json.load(file)

            # 如果 json_data 是一个列表，遍历每个项目
            if isinstance(json_data, list):
                for entry in json_data:
                    document_id = entry.get("document_id", Path(json_file).stem)
                    content = json.dumps(entry, indent=2)  # 将整个 entry 存储为文本

                    # 处理列表类型的元数据字段，将其转换为逗号分隔的字符串
                    tags = entry.get("tags", [])
                    if isinstance(tags, list):
                        tags = ", ".join(tags)  # 转换为逗号分隔的字符串

                    # 处理字典类型的元数据字段，将其转换为字符串
                    metadata_dict = entry.get("metadata", {})
                    if isinstance(metadata_dict, dict):
                        metadata_str = "; ".join([f"{k}: {v}" for k, v in metadata_dict.items()])

                    metadata = {
                        "document_id": document_id,
                        "title": entry.get("title", "Untitled"),
                        "author": entry.get("author", "Unknown"),
                        "date": entry.get("date", "Unknown"),
                        "tags": tags,
                        "abstract": entry.get("abstract", ""),
                        "metadata": metadata_str,  # 存储为字符串
                        "url": entry.get("url", ""),
                        "source": str(json_file)
                    }
                    json_document = Document(page_content=content, metadata=metadata)
                    json_documents.append(json_document)
            else:
                print(f"Unexpected JSON structure in {json_file}, skipping...")

    print(f"Loaded {len(json_documents)} JSON documents.")
    return json_documents
