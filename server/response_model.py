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
    vs_type: str  # 向量库类型
    embed_model: str  # Embeddings模型

class DeleteFilesRequest(BaseModel):
    kb_name: str
    files: List[Dict[str, str]]

class ChatRequest(BaseModel):
    prompt: str
    tools: list = None
    model: str = "default"
    use_self_model: bool = False
    use_local_model: bool = False

class ChatResponse(BaseModel):
    # 根据模式不同，返回不同的字段
    answer: str = None
    chunks: list = None
    references: list = None
    error: str = None

# 获取文档
class DocumentRequest(BaseModel):
    source: str

class DocumentResponse(BaseModel):
    content: str


