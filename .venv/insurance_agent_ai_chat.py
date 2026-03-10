import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置火山引擎API密钥
VOLC_API_KEY = os.getenv("VOLC_API_KEY")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

def insurance_agent_chat(user_input):
    """
    保险代理人AI智能问答功能（使用免费API额度）
    :param user_input: 用户的问题或需求
    :return: AI的回答
    """
    # 构建请求URL
    url = f"https://ark.cn-beijing.volces.com/api/v3/chat/completions" 

    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {VOLC_API_KEY}"
    }

    # 构建请求体
    data = {
        "model": ENDPOINT_ID,
        "messages": [
            {
                "role": "system",
                "content": """
                你是一位专业的保险代理人AI智能助手，你的任务是帮助保险代理人回答客户的问题，提供专业的保险咨询服务。
                请站在保险代理人的立场，以专业、友好、易懂的语言回答客户的问题。
                不要站在保险公司的立场，不要推销特定的保险产品。
                """
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    # 发送请求
    response = requests.post(url, headers=headers, json=data)

    # 返回AI的回答
    return response.json()["choices"][0]["message"]["content"].strip()

# 测试功能
if __name__ == "__main__":
    user_input = "请问购买重疾险需要注意哪些事项？"
    ai_response = insurance_agent_chat(user_input)
    print("AI回答：", ai_response)