from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import sys
# 将ai_assistant目录添加到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), "ai_assistant"))
# 直接导入core模块中的AIAssistant
from core import AIAssistant

# 加载环境变量
load_dotenv()

# 初始化FastAPI应用
app = FastAPI(title="保险代理人AI智能助手", version="1.0")

# 初始化AI助手
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "wenxin")
AI_ASSISTANT = AIAssistant(
    model_type=DEFAULT_MODEL,
    api_keys={
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "baidu_api_key": os.getenv("BAIDU_API_KEY"),
        "baidu_secret_key": os.getenv("BAIDU_SECRET_KEY"),
        "tongyi_api_key": os.getenv("TONGYI_API_KEY"),
        "hf_api_token": os.getenv("HF_API_TOKEN"),
        "hf_repo_id": os.getenv("HF_REPO_ID"),
        "doubao_api_key": os.getenv("DOUBAO_API_KEY")
    }
)

# 定义请求模型
class QuestionRequest(BaseModel):
    question: str
    context: str = None
    model_type: str = DEFAULT_MODEL

# 定义响应模型
class AnswerResponse(BaseModel):
    question: str
    answer: str
    model_type: str

# 问答接口
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """AI问答接口"""
    try:
        # 如果指定了不同的模型类型，创建新的AI助手实例
        if request.model_type != DEFAULT_MODEL:
            assistant = AIAssistant(
                model_type=request.model_type,
                api_keys={
                    "openai_api_key": os.getenv("OPENAI_API_KEY"),
                    "baidu_api_key": os.getenv("BAIDU_API_KEY"),
                    "baidu_secret_key": os.getenv("BAIDU_SECRET_KEY"),
                    "tongyi_api_key": os.getenv("TONGYI_API_KEY"),
                    "hf_api_token": os.getenv("HF_API_TOKEN"),
                    "hf_repo_id": os.getenv("HF_REPO_ID"),
                    "doubao_api_key": os.getenv("DOUBAO_API_KEY")
                }
            )
            answer = assistant.ask(request.question, request.context)
        else:
            answer = AI_ASSISTANT.ask(request.question, request.context)
        
        return AnswerResponse(
            question=request.question,
            answer=answer,
            model_type=request.model_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI助手出错：{str(e)}")

# 健康检查接口
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "model_type": DEFAULT_MODEL}

# 运行应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)