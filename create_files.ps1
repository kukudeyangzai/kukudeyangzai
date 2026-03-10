# 创建项目根目录下的文件
New-Item -Path "main.py" -ItemType File -Force
Set-Content -Path "main.py" -Value @"
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import sys
# 将ai_assistant目录添加到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), "ai_assistant"))
# 直接导入core模块中的AIAssistant类
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
"@

New-Item -Path "requirements.txt" -ItemType File -Force
Set-Content -Path "requirements.txt" -Value @"
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
openai==1.3.0
langchain==0.1.0
langchain-community==0.0.10
requests==2.31.0
"@

New-Item -Path ".env.example" -ItemType File -Force
Set-Content -Path ".env.example" -Value @"
# OpenAI配置
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 百度文心一言配置
BAIDU_API_KEY=你的百度API密钥
BAIDU_SECRET_KEY=你的百度Secret密钥

# 阿里通义千问配置
TONGYI_API_KEY=你的阿里通义千问API密钥

# Hugging Face配置
HF_API_TOKEN=你的Hugging Face API密钥
HF_REPO_ID=meta-llama/Meta-Llama-3-8B-Instruct

# 豆包大模型配置
DOUBAO_API_KEY=你的豆包API密钥

# 默认模型
DEFAULT_MODEL=wenxin  # 可选值：openai, wenxin, tongyi, huggingface, doubao
"@

New-Item -Path ".env" -ItemType File -Force
Set-Content -Path ".env" -Value @"
# 请填写你的API密钥
"@

# 创建ai_assistant目录下的文件
New-Item -Path "ai_assistant" -ItemType Directory -Force

New-Item -Path "ai_assistant\core.py" -ItemType File -Force
Set-Content -Path "ai_assistant\core.py" -Value @"
from typing import Dict, Optional
# 直接导入同级模块，无需__init__.py
from openai_client import OpenAIClient
from wenxin_client import WenxinClient
from tongyi_client import TongyiClient
from huggingface_client import HuggingFaceClient
from doubao_client import DoubaoClient

class AIAssistant:
    """统一的AI助手接口，支持多模型切换"""
    
    def __init__(self, model_type: str = "wenxin", api_keys: Optional[Dict] = None):
        """
        初始化AI助手
        :param model_type: 模型类型，可选"openai", "wenxin", "tongyi", "huggingface", "doubao"
        :param api_keys: API密钥字典
        """
        self.model_type = model_type
        self.api_keys = api_keys or {}
        self.client = self._init_client()
    
    def _init_client(self):
        """根据模型类型初始化对应的客户端"""
        if self.model_type == "openai":
            return OpenAIClient(
                api_key=self.api_keys.get("openai_api_key")
            )
        elif self.model_type == "wenxin":
            return WenxinClient(
                api_key=self.api_keys.get("baidu_api_key"),
                secret_key=self.api_keys.get("baidu_secret_key")
            )
        elif self.model_type == "tongyi":
            return TongyiClient(
                api_key=self.api_keys.get("tongyi_api_key")
            )
        elif self.model_type == "huggingface":
            return HuggingFaceClient(
                api_token=self.api_keys.get("hf_api_token"),
                repo_id=self.api_keys.get("hf_repo_id")
            )
        elif self.model_type == "doubao":
            return DoubaoClient(
                api_key=self.api_keys.get("doubao_api_key")
            )
        else:
            raise ValueError(f"不支持的模型类型：{self.model_type}")
    
    def ask(self, question: str, context: Optional[str] = None) -> str:
        """
        回答客户问题
        :param question: 客户问题
        :param context: 上下文信息（可选）
        :return: AI回答
        """
        # 构建完整的提示词，站在个人代理人的立场
        prompt = self._build_prompt(question, context)
        return self.client.generate(prompt)
    
    def _build_prompt(self, question: str, context: Optional[str] = None) -> str:
        """构建符合代理人立场的提示词"""
        base_prompt = """你是一位专业的保险代理人AI助手，请站在代理人的立场回答客户的问题。
        回答要专业、客观、易懂，避免使用专业术语，站在客户的角度考虑问题。"""
        
        if context:
            base_prompt += f"\n\n上下文信息：{context}"
        
        base_prompt += f"\n\n客户问题：{question}\n\n回答："
        return base_prompt
"@

New-Item -Path "ai_assistant\openai_client.py" -ItemType File -Force
Set-Content -Path "ai_assistant\openai_client.py" -Value @"
from openai import OpenAI

class OpenAIClient:
    """OpenAI客户端"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def generate(self, prompt: str) -> str:
        """生成回答"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
"@

New-Item -Path "ai_assistant\wenxin_client.py" -ItemType File -Force
Set-Content -Path "ai_assistant\wenxin_client.py" -Value @"
from langchain.llms import Wenxin

class WenxinClient:
    """百度文心一言客户端"""
    
    def __init__(self, api_key: str, secret_key: str):
        self.llm = Wenxin(
            model="ernie-bot-4",
            baidu_api_key=api_key,
            baidu_secret_key=secret_key
        )
    
    def generate(self, prompt: str) -> str:
        """生成回答"""
        return self.llm.invoke(prompt).strip()
"@

New-Item -Path "ai_assistant\tongyi_client.py" -ItemType File -Force
Set-Content -Path "ai_assistant\tongyi_client.py" -Value @"
from langchain.llms import Tongyi

class TongyiClient:
    """阿里通义千问客户端"""
    
    def __init__(self, api_key: str):
        self.llm = Tongyi(
            model="qwen-plus",
            dashscope_api_key=api_key
        )
    
    def generate(self, prompt: str) -> str:
        """生成回答"""
        return self.llm.invoke(prompt).strip()
"@

New-Item -Path "ai_assistant\huggingface_client.py" -ItemType File -Force
Set-Content -Path "ai_assistant\huggingface_client.py" -Value @"
from langchain.llms import HuggingFaceHub

class HuggingFaceClient:
    """Hugging Face客户端"""
    
    def __init__(self, api_token: str, repo_id: str):
        self.llm = HuggingFaceHub(
            repo_id=repo_id,
            model_kwargs={"temperature": 0.7, "max_tokens": 1024},
            huggingfacehub_api_token=api_token
        )
    
    def generate(self, prompt: str) -> str:
        """生成回答"""
        return self.llm.invoke(prompt).strip()
"@

New-Item -Path "ai_assistant\doubao_client.py" -ItemType File -Force
Set-Content -Path "ai_assistant\doubao_client.py" -Value @"
import requests
import json
from typing import Optional

class DoubaoClient:
    """豆包大模型客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.doubao.com/v1/chat/completions" 
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def generate(self, prompt: str, model: str = "doubao-3") -> str:
        """
        生成回答
        :param prompt: 提示词
        :param model: 模型版本，可选"doubao-3", "doubao-3-turbo"
        :return: AI回答
        """
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise RuntimeError(f"豆包API调用失败：{str(e)}")
"@