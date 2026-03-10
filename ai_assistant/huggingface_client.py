from langchain.llms import HuggingFaceHub

class HuggingFaceClient:
    """Hugging Face客户�?""
    
    def __init__(self, api_token: str, repo_id: str):
        self.llm = HuggingFaceHub(
            repo_id=repo_id,
            model_kwargs={"temperature": 0.7, "max_tokens": 1024},
            huggingfacehub_api_token=api_token
        )
    
    def generate(self, prompt: str) -> str:
        """生成回答"""
        return self.llm.invoke(prompt).strip()
