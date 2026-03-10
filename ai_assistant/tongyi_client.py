from langchain.llms import Tongyi

class TongyiClient:
    """阿里通义千问客户�?""
    
    def __init__(self, api_key: str):
        self.llm = Tongyi(
            model="qwen-plus",
            dashscope_api_key=api_key
        )
    
    def generate(self, prompt: str) -> str:
        """生成回答"""
        return self.llm.invoke(prompt).strip()
