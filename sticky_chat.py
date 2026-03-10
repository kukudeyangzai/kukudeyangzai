import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 读取配置
api_key = os.getenv("ARK_API_KEY")
endpoint_id = os.getenv("ENDPOINT_ID")

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

def chat_with_style(user_input, style="professional"):
    """
    根据指定风格生成回复
    
    风格类型：
    - professional: 专业版（适合与同行或资深客户沟通）
    - simple: 通俗版（适合给保险小白解释）
    - empathic: 共情版（适合安抚客户情绪）
    """
    
    # 风格提示词配置
    style_prompts = {
        "professional": "你是一位资深的保险专家，请用专业、严谨的语言回答问题，适当使用专业术语，体现专业深度。",
        "simple": "你是一位擅长用大白话解释保险的代理人，请用通俗易懂的语言回答，多用生活化的比喻，避免专业术语，让普通人一听就懂。",
        "empathic": "你是一位非常贴心、善于共情的保险顾问，请用温暖、关怀的语气回答，先理解客户的担忧和感受，再提供建议，让客户感受到被理解。"
    }
    
    try:
        response = client.chat.completions.create(
            model=endpoint_id,
            messages=[
                {"role": "system", "content": style_prompts[style]},
                {"role": "user", "content": user_input}
            ],
            temperature=0.8,  # 稍微提高温度，让回复更有风格差异
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败：{e}"

def main():
    print("=" * 60)
    print("      保险代理人智能助手 v0.2 - 三种话术风格")
    print("=" * 60)
    print("支持风格：")
    print("1. 专业版 - 严谨专业，适合专业沟通")
    print("2. 通俗版 - 大白话解释，适合客户科普")
    print("3. 共情版 - 温暖关怀，适合安抚客户")
    print("-" * 60)
    
    while True:
        print("\n" + "-" * 60)
        user_input = input("请输入你的问题（输入q退出）：").strip()
        
        if user_input.lower() == 'q':
            print("感谢使用，再见！")
            break
        
        if not user_input:
            continue
        
        print("\n正在生成三种风格的回复...\n")
        
        # 生成三种风格的回复
        professional = chat_with_style(user_input, "professional")
        simple = chat_with_style(user_input, "simple")
        empathic = chat_with_style(user_input, "empathic")
        
        # 打印结果
        print("=" * 60)
        print("📌 【专业版】（适合专业沟通）")
        print("-" * 40)
        print(professional)
        
        print("\n📌 【通俗版】（适合客户科普）")
        print("-" * 40)
        print(simple)
        
        print("\n📌 【共情版】（适合安抚客户）")
        print("-" * 40)
        print(empathic)
        print("=" * 60)

if __name__ == "__main__":
    main()