from fastapi import FastAPI
from pydantic import BaseModel
from chat import generate_response  # 导入对话生成的逻辑

app = FastAPI()

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

if __name__ == "__main__":
    import uvicorn
    # 启动API服务
    uvicorn.run(app, host="0.0.0.0", port=8000)
