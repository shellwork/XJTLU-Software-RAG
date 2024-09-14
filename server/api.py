import sys
from pathlib import Path
import logging

from chat import generate_response

# 获取当前文件所在目录的上两级目录（项目根目录）
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root))  # 将根目录添加到系统路径中

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Dict
from create_database import (
    initialize_upload_path, save_file_to_category, create_kb,
    get_kb_list, get_kb_documents, delete_kb, delete_kb_files,
    delete_existing_chroma, generate_data_store
)
from response_model import CreateKnowledgeBaseModel, DeleteFilesRequest, ChatResponse, ChatRequest

# 配置日志记录
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

app = FastAPI(debug=True)  # 启用调试模式


# 定义聊天API接口
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 调用生成对话的函数，传入用户的输入和工具等信息
    ai_response = generate_response(
        request.prompt,
        request.tools,
        request.model,
        use_self_model=request.use_self_model,
        use_local_model=request.use_local_model
    )
    # 返回AI生成的响应
    return ChatResponse(response=ai_response)


# 启动时初始化上传路径
@app.on_event("startup")
def startup_event():
    initialize_upload_path()
    logging.info("上传路径初始化完成")



# 上传文件 API
@app.post("/upload_files")
def upload_files(kb_name: str = Form(...), files: List[UploadFile] = File(...)):
    logging.debug(f"上传文件请求: kb_name={kb_name}, 文件数量={len(files)}")
    for file in files:
        save_file_to_category(file, kb_name)
        logging.info(f"文件 {file.filename} 已保存至知识库 {kb_name}")
    return {"status": "success", "message": f"{len(files)} 文件上传成功至知识库 {kb_name}"}

# 创建知识库 API
@app.post("/create_kb")
def api_create_kb(kb_info: CreateKnowledgeBaseModel):
    logging.debug(f"创建知识库请求: {kb_info}")
    result = create_kb(kb_info)
    if result["status"] == "success":
        logging.info(f"知识库 {kb_info.kb_name} 创建成功")
    else:
        logging.warning(f"知识库创建失败: {result['message']}")
    return result

# 获取知识库列表 API
@app.get("/get_kb_list")
def api_get_kb_list():
    logging.debug("获取知识库列表请求")
    kb_list = get_kb_list()
    logging.info(f"获取到 {len(kb_list)} 个知识库")
    return kb_list

# 获取知识库中的文档 API
@app.get("/get_kb_documents")
def api_get_kb_documents(kb_name: str):
    logging.debug(f"获取知识库文档请求: kb_name={kb_name}")
    documents = get_kb_documents(kb_name)
    if isinstance(documents, list):
        logging.info(f"知识库 {kb_name} 包含 {len(documents)} 个文件")
    else:
        logging.warning(f"获取知识库文档失败: {documents['message']}")
    return documents

# 重建向量库 API
@app.post("/rebuild_vector_store")
def api_rebuild_vector_store(kb_name: str):
    logging.debug(f"重建向量库请求: kb_name={kb_name}")
    if kb_name not in get_kb_list():
        logging.error(f"知识库 {kb_name} 不存在")
        return {"status": "error", "message": "知识库不存在"}

    delete_existing_chroma()
    generate_data_store()
    logging.info(f"向量库已成功为知识库 {kb_name} 重建")
    return {"status": "success", "message": f"向量库已成功为知识库 {kb_name} 重建"}

# 删除知识库 API
@app.post("/delete_kb")
def api_delete_kb(kb_name: str = Form(...)):  # 使用 Form 来接收表单数据中的字符串
    logging.debug(f"删除知识库请求: kb_name={kb_name}")
    result = delete_kb(kb_name)
    if result["status"] == "success":
        logging.info(f"知识库 {kb_name} 已删除")
    else:
        logging.warning(f"删除知识库失败: {result['message']}")
    return result

# 删除知识库中的文件 API
@app.post("/delete_kb_files")
def api_delete_kb_files(request: DeleteFilesRequest):
    try:
        logging.debug(f"删除文件请求: kb_name={request.kb_name}, files={request.files}")
        result = delete_kb_files(request.kb_name, request.files)
        if result["status"] == "success":
            logging.info(f"文件已成功从知识库 {request.kb_name} 中删除")
        else:
            logging.warning(f"删除文件失败: {result['message']}")
        return result
    except Exception as e:
        logging.error(f"删除文件时出现异常: {e}", exc_info=True)
        return {"status": "error", "message": f"删除文件时发生错误: {str(e)}"}

# 启动 FastAPI 服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
