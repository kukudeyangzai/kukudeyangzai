import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 读取配置
api_key = os.getenv("ARK_API_KEY")
endpoint_id = os.getenv("ENDPOINT_ID")

# 简单打印（不做过多的格式检查）
print(f"使用接入点: {endpoint_id}")
print("-" * 50)

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

# 发起问答
try:
    response = client.chat.completions.create(
        model=endpoint_id,
        messages=[
            {"role": "user", "content": "请用一句话介绍什么是重疾险"}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    print("\n" + "="*50)
    print("AI回答：")
    print(response.choices[0].message.content)
    print("="*50)
    
except Exception as e:
    print(f"出错了：{e}")