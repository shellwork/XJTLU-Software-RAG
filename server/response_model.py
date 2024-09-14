from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class BaseResponse(BaseModel):
    code: int
    msg: str
    data: Optional[Any] = None

class ListResponse(BaseModel):
    code: int
    msg: str
    data: List[Any]

class CreateKnowledgeBaseModel(BaseModel):
    kb_name: str
    kb_info: str
    vs_type: str
    embed_model: str

class DeleteFilesRequest(BaseModel):
    kb_name: str
    files: List[Dict[str, str]]

# 定义请求体模型
class ChatRequest(BaseModel):
    prompt: str
    tools: list = []  # 默认是空的工具列表
    model: str = "default"  # 默认模型名称
    use_self_model: bool = False  # 增加 use_self_model 字段
    use_local_model: bool = False  # 增加 use_local_model 字段

# 定义响应体模型
class ChatResponse(BaseModel):
    response: str