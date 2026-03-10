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
        :param prompt: 提示�?
        :param model: 模型版本，可�?doubao-3", "doubao-3-turbo"
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
