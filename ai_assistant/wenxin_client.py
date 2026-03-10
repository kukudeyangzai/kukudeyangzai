from langchain.llms import Wenxin

class WenxinClient:
    """百度文心一言客户�?""
    
    def __init__(self, api_key: str, secret_key: str):
        self.llm = Wenxin(
            model="ernie-bot-4",
            baidu_api_key=api_key,
            baidu_secret_key=secret_key
        )
    
    def generate(self, prompt: str) -> str:
        """生成回答"""
        return self.llm.invoke(prompt).strip()
