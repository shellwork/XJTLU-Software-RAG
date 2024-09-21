import sys
import uuid
from pathlib import Path
import logging
from urllib.parse import unquote_plus

from fastapi.staticfiles import StaticFiles
from chat import generate_response

# 获取当前文件所在上两级目录（项目根目录）
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root))  # 将根目录添加到系统路径中
from fastapi import UploadFile, File, Form, Query, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from create_database import (
    initialize_upload_path, save_file_to_category, create_kb,
    get_kb_list, get_kb_documents, delete_kb, delete_kb_files,
    delete_existing_chroma, update_kb_metadata, process_batches
)
from response_model import CreateKnowledgeBaseModel, DeleteFilesRequest, ChatResponse, ChatRequest, DocumentResponse

# 配置日志记录
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

app = FastAPI()

# 挂载静态文件目录，方便直接访问文件
DATA_PATH = Path("data/uploads").resolve()
DATA_PATH.mkdir(parents=True, exist_ok=True)  # 确保目录存在
app.mount("/uploads", StaticFiles(directory=DATA_PATH), name="uploads")


# 定义聊天API接口
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    ai_response = generate_response(
        prompt=request.prompt,
        tools=request.tools,
        model=request.model,
        use_self_model=request.use_self_model,
        use_local_model=request.use_local_model
    )
    return ChatResponse(**ai_response)


# 获取文档
@app.get("/api/document", response_model=DocumentResponse)
async def get_document(source: str = Query(..., description="文档的路径，格式为 知识库名称/文件类型/文件名")):
    """
    根据 source 参数获取文档内容。
    source 格式: 知识库名称/文件类型/文件名
    """
    try:
        from config import DATA_PATH

        # 解码 URL 中的 source 参数
        source_decoded = unquote_plus(source)

        # 确保 DATA_PATH 是 Path 对象
        DATA_PATH = Path(DATA_PATH) if isinstance(DATA_PATH, str) else DATA_PATH

        # 组合解码后的路径
        document_path = (DATA_PATH / source_decoded).resolve()
        logging.debug(f"尝试读取文档: {document_path}")

        # 防止路径遍历攻击
        if not document_path.is_relative_to(DATA_PATH):
            logging.warning(f"非法的文档路径尝试: {document_path}")
            raise HTTPException(status_code=400, detail="非法的文档路径。")

        # 检查文件是否存在并且是文件
        if document_path.exists() and document_path.is_file():
            file_extension = document_path.suffix.lower()
            if file_extension in ['.txt', '.md', '.py', '.json', '.csv']:
                # 读取文本文件
                content = document_path.read_text(encoding='utf-8')
                logging.info(f"成功读取文本文档: {document_path}")
                return DocumentResponse(content=content)
            elif file_extension in ['.pdf', '.png', '.jpg', '.jpeg', '.gif']:
                # 返回文件的 URL，供前端直接访问
                document_url = f"http://localhost:8000/uploads/{source}"
                logging.info(f"成功获取文件链接: {document_url}")
                return DocumentResponse(content=document_url)
            else:
                # 默认处理为文本
                content = document_path.read_text(encoding='utf-8')
                logging.info(f"成功读取未知类型文档: {document_path}")
                return DocumentResponse(content=content)
        else:
            logging.warning(f"文档不存在: {document_path}")
            raise HTTPException(status_code=404, detail="文档不存在。")
    except Exception as e:
        logging.error(f"获取文档内容时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取文档内容时出错: {str(e)}")


# 启动时初始化上传路径
@app.on_event("startup")
def startup_event():
    initialize_upload_path()
    logging.info("上传路径初始化完成")


# 上传文件 API
@app.post("/upload_files")
async def upload_files(
        kb_name: str = Form(...),
        files: List[UploadFile] = File(...),
        chunk_size: int = Form(100),  # 默认值为100
        chunk_overlap: int = Form(20),  # 默认值为20
        zh_title_enhance: bool = Form(False)  # 默认值为 False
):
    logging.debug(
        f"上传文件请求: kb_name={kb_name}, 文件数量={len(files)}, chunk_size={chunk_size}, chunk_overlap={chunk_overlap}, zh_title_enhance={zh_title_enhance}")
    relative_paths = []
    try:
        # 为该批次创建一个唯一的批次 ID
        batch_id = str(uuid.uuid4())

        # 保存文件
        files_names = []  # 初始化为列表
        for file in files:
            file_name = save_file_to_category(file, kb_name)  # 单个文件名
            if file_name:  # 确保文件保存成功并返回了文件名
                files_names.append(file_name)  # 将文件名添加到列表中
            logging.info(f"文件 {file.filename} 已保存至知识库 {kb_name}")

        # 将该批次的配置信息保存到元数据文件中
        batch_metadata = {
            "batch_id": batch_id,
            "files": files_names,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "zh_title_enhance": zh_title_enhance
        }
        # 记录到知识库的元数据中
        update_kb_metadata(kb_name, batch_metadata, is_batch=True)

        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": f"{len(files)} 文件上传成功至知识库 {kb_name}",
            "batch_id": batch_id,  # 返回批次 ID
            "paths": relative_paths
        })
    except Exception as e:
        logging.error(f"上传文件时出错: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"status": "error", "message": f"上传文件时发生错误: {str(e)}"})


# 创建知识库 API
@app.post("/create_kb")
def api_create_kb(kb_info: CreateKnowledgeBaseModel):
    logging.debug(f"创建知识库请求: {kb_info}")
    # 调用 create_kb 函数，传递 embed_model 和其他参数
    result = create_kb(
        kb_name=kb_info.kb_name,
        kb_info=kb_info.kb_info,
        vs_type=kb_info.vs_type,
        embed_model=kb_info.embed_model
    )

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
def api_rebuild_vector_store(kb_name: str, action: bool = False):
    logging.debug(f"重建向量库请求: kb_name={kb_name}, action={action}")
    if kb_name not in get_kb_list():
        logging.error(f"知识库 {kb_name} 不存在")
        return {"status": "error", "message": "知识库不存在"}
    if action:
        print("delete chroma")
        delete_existing_chroma()
    # 调用 create_database 模块中的函数进行分块和向量化处理
    result = process_batches(kb_name)
    if result["status"] == "success":
        logging.info(f"向量库已成功从知识库 {kb_name} 更新")
    else:
        logging.error(f"更新向量库时出错: {result['message']}")

    return result


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
