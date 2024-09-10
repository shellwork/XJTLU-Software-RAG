from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List
from create_database import (
    initialize_upload_path, save_file_to_category, create_kb,
    get_kb_list, get_kb_documents, delete_kb, delete_kb_files,
    delete_existing_chroma, generate_data_store
)

app = FastAPI()


# 启动时初始化上传路径
@app.on_event("startup")
def startup_event():
    initialize_upload_path()


# 定义请求体模型
class CreateKnowledgeBase(BaseModel):
    kb_name: str
    kb_info: str
    vs_type: str
    embed_model: str


# 上传文件 API
@app.post("/upload_files")
def upload_files(kb_name: str = Form(...), files: List[UploadFile] = File(...)):
    for file in files:
        save_file_to_category(file, kb_name)
    return {"status": "success", "message": f"{len(files)} 文件上传成功至知识库 {kb_name}"}


# 创建知识库 API
@app.post("/create_kb")
def api_create_kb(kb_info: CreateKnowledgeBase):
    result = create_kb(kb_info)
    return result


# 获取知识库列表 API
@app.get("/get_kb_list")
def api_get_kb_list():
    return get_kb_list()


# 获取知识库中的文档 API
@app.get("/get_kb_documents")
def api_get_kb_documents(kb_name: str):
    return get_kb_documents(kb_name)


# 重建向量库 API
@app.post("/rebuild_vector_store")
def api_rebuild_vector_store(kb_name: str):
    if kb_name not in get_kb_list():
        return {"status": "error", "message": "知识库不存在"}

    delete_existing_chroma()
    generate_data_store()
    return {"status": "success", "message": f"向量库已成功为知识库 {kb_name} 重建"}


# 删除知识库 API
@app.post("/delete_kb")
def api_delete_kb(kb_name: str):
    return delete_kb(kb_name)


# 删除知识库中的文件 API
@app.post("/delete_kb_files")
def api_delete_kb_files(kb_name: str, files: List[str]):
    return delete_kb_files(kb_name, files)


# 启动 FastAPI 服务
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
