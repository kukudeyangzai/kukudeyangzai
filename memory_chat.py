import os
import json
from datetime import datetime
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

class InsuranceAgent:
    """保险代理人智能助手（带记忆功能）"""
    
    def __init__(self, agent_name="我的助手"):
        self.agent_name = agent_name
        self.conversation_history = []  # 存储当前对话历史
        self.style = "professional"  # 默认风格
        
        # 风格提示词
        self.style_prompts = {
            "professional": "你是一位资深的保险专家，请用专业、严谨的语言回答问题，适当使用专业术语。",
            "simple": "你是一位擅长用大白话解释保险的代理人，请用通俗易懂的语言回答，多用生活化的比喻。",
            "empathic": "你是一位非常贴心、善于共情的保险顾问，请用温暖、关怀的语气回答，先理解客户的担忧。"
        }
    
    def set_style(self, style):
        """切换对话风格"""
        if style in self.style_prompts:
            self.style = style
            return f"已切换到【{style}】风格"
        return "风格不存在，可选：professional/simple/empathic"
    
    def add_message(self, role, content):
        """添加消息到历史记录"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "time": datetime.now().strftime("%H:%M:%S")
        })
    
    def chat(self, user_input):
        """发送消息并获取回复"""
        
        # 构建消息列表
        messages = []
        
        # 添加系统提示词（当前风格）
        messages.append({"role": "system", "content": self.style_prompts[self.style]})
        
        # 添加上下文历史（最多保留最近10轮）
        for msg in self.conversation_history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # 添加当前用户输入
        messages.append({"role": "user", "content": user_input})
        
        try:
            # 调用API
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=messages,
                temperature=0.8,
                max_tokens=1000
            )
            
            ai_reply = response.choices[0].message.content
            
            # 保存到历史记录
            self.add_message("user", user_input)
            self.add_message("assistant", ai_reply)
            
            return ai_reply
            
        except Exception as e:
            error_msg = f"出错了：{e}"
            return error_msg
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        return "对话历史已清空"
    
    def save_conversation(self, filename=None):
        """保存对话记录到文件"""
        if not filename:
            filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        
        return f"对话已保存到 {filename}"
    
    def show_history(self):
        """显示最近的对话历史"""
        if not self.conversation_history:
            return "暂无对话历史"
        
        output = "\n📝 最近对话：\n"
        for msg in self.conversation_history[-6:]:  # 显示最近6条
            role_symbol = "👤" if msg["role"] == "user" else "🤖"
            output += f"{role_symbol} [{msg['time']}] {msg['content'][:50]}...\n"
        
        return output

def main():
    print("=" * 60)
    print("      保险代理人智能助手 v0.3 - 多轮对话版")
    print("=" * 60)
    print("✨ 新功能：")
    print("  • 记住对话上下文，连续提问")
    print("  • 支持切换三种风格")
    print("  • 可保存对话记录")
    print("-" * 60)
    
    # 初始化助手
    agent = InsuranceAgent()
    
    # 命令帮助
    print("\n🛠️ 可用命令：")
    print("  /style 专业版   - 切换风格（专业版/通俗版/共情版）")
    print("  /clear          - 清空对话历史")
    print("  /save           - 保存对话记录")
    print("  /history        - 查看最近对话")
    print("  /help           - 显示帮助")
    print("  /quit 或 q      - 退出程序")
    print("-" * 60)
    
    while True:
        print("\n" + "-" * 60)
        user_input = input("你：").strip()
        
        # 处理退出命令
        if user_input.lower() in ['/quit', 'q']:
            print("感谢使用，再见！")
            break
        
        # 处理命令
        if user_input.startswith('/'):
            cmd = user_input.lower()
            
            if cmd == '/clear':
                print(agent.clear_history())
                
            elif cmd == '/save':
                print(agent.save_conversation())
                
            elif cmd == '/history':
                print(agent.show_history())
                
            elif cmd == '/help':
                print("\n可用命令：")
                print("  /style 专业版   - 切换风格")
                print("  /clear          - 清空历史")
                print("  /save           - 保存对话")
                print("  /history        - 查看历史")
                print("  /quit 或 q      - 退出")
                
            elif cmd.startswith('/style'):
                style_name = user_input[7:].strip()  # 去掉'/style '
                if style_name == "专业版":
                    result = agent.set_style("professional")
                elif style_name == "通俗版":
                    result = agent.set_style("simple")
                elif style_name == "共情版":
                    result = agent.set_style("empathic")
                else:
                    result = "请输入：专业版 / 通俗版 / 共情版"
                print(result)
            
            continue  # 跳过普通对话处理
        
        # 普通对话
        if not user_input:
            continue
        
        print("\n🤖 助手正在思考...")
        reply = agent.chat(user_input)
        print(f"\n🤖 助手：{reply}")

if __name__ == "__main__":
    main()