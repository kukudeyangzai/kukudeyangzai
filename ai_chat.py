import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量（从.env文件中读取密钥和接入点ID）
load_dotenv()

# 从环境变量中读取API密钥和接入点ID
ARK_API_KEY = os.getenv("ARK_API_KEY")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

# 初始化OpenAI客户端（火山引擎兼容OpenAI格式）
client = OpenAI(
    api_key=ARK_API_KEY,
    base_url="https://ark.cn-beijing.volces.com/api/v3"  # 火山引擎方舟的API地址
)

def chat_with_ai(user_input):
    """调用火山引擎大模型进行对话"""
    try:
        # 发起对话请求
        response = client.chat.completions.create(
            model=ENDPOINT_ID,  # 使用接入点ID指定模型
            messages=[
                {"role": "system", "content": "你是一个专业的保险顾问，精通各类保险知识，请用通俗易懂的语言回答用户问题。"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,  # 控制回复的随机性，0.7为平衡模式[citation:3]
            max_tokens=1000   # 限制回复最大长度[citation:3]
        )
        
        # 提取AI的回复内容[citation:4]
        ai_response = response.choices[0].message.content
        return ai_response
        
    except Exception as e:
        return f"API调用出错：{str(e)}"

def main():
    """主函数：循环接收用户输入并获取AI回答"""
    print("=" * 50)
    print("保险智能助手已启动（输入 q 退出）")
    print("=" * 50)
    
    while True:
        # 获取用户输入
        user_input = input("\n请输入你的问题（输入q退出）：").strip()
        
        # 检查是否退出
        if user_input.lower() == 'q':
            print("感谢使用，再见！")
            break
        
        # 跳过空输入
        if not user_input:
            print("请输入有效问题")
            continue
        
        # 调用AI并输出回答
        print("\nAI回答：", end="")
        response = chat_with_ai(user_input)
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    main()