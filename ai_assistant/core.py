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
        :param model_type: 模型类型，可�?openai", "wenxin", "tongyi", "huggingface", "doubao"
        :param api_keys: API密钥字典
        """
        self.model_type = model_type
        self.api_keys = api_keys or {}
        self.client = self._init_client()
    
    def _init_client(self):
        """根据模型类型初始化对应的客户�?""
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
        # 构建完整的提示词，站在个人代理人的立�?
        prompt = self._build_prompt(question, context)
        return self.client.generate(prompt)
    
    def _build_prompt(self, question: str, context: Optional[str] = None) -> str:
        """构建符合代理人立场的提示�?""
        base_prompt = """你是一位专业的保险代理人AI助手，请站在代理人的立场回答客户的问题�?
        回答要专业、客观、易懂，避免使用专业术语，站在客户的角度考虑问题�?""
        
        if context:
            base_prompt += f"\n\n上下文信息：{context}"
        
        base_prompt += f"\n\n客户问题：{question}\n\n回答�?
        return base_prompt
