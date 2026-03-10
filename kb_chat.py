import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# PDF支持库
from pypdf import PdfReader

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

class InsuranceKnowledgeBase:
    """保险知识库管理器（支持PDF和TXT）"""
    
    def __init__(self, kb_path="./knowledge_base"):
        self.kb_path = kb_path
        self.documents = {}  # 存储文档 {文件名: 内容}
        
        # 创建知识库文件夹
        if not os.path.exists(kb_path):
            os.makedirs(kb_path)
            print(f"创建知识库文件夹: {kb_path}")
        
        # 加载所有文档
        self._load_all_documents()
    
    def _load_all_documents(self):
        """加载知识库中的所有文档（支持PDF和TXT）"""
        if not os.path.exists(self.kb_path):
            return
        
        print("\n📚 正在加载知识库文档...")
        for filename in os.listdir(self.kb_path):
            file_path = os.path.join(self.kb_path, filename)
            
            # 处理TXT文件
            if filename.endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.documents[filename] = f.read()
                    print(f"  ✅ 已加载TXT: {filename}")
                except Exception as e:
                    print(f"  ❌ 加载失败 {filename}: {e}")
            
            # 处理PDF文件
            elif filename.endswith('.pdf'):
                try:
                    content = self._read_pdf(file_path)
                    if content:
                        # 保存为同名的txt副本，方便下次快速加载
                        txt_filename = filename.replace('.pdf', '.txt')
                        txt_path = os.path.join(self.kb_path, txt_filename)
                        with open(txt_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        self.documents[txt_filename] = content
                        print(f"  ✅ 已加载PDF并转换: {filename}")
                except Exception as e:
                    print(f"  ❌ PDF加载失败 {filename}: {e}")
        
        print(f"📊 共加载 {len(self.documents)} 个文档\n")
    
    def _read_pdf(self, pdf_path):
        """读取PDF文件内容"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"PDF读取错误: {e}")
            return None
    
    def add_document(self, title, content, file_type='txt'):
        """添加新文档到知识库"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if file_type == 'txt':
            filename = f"{title}_{timestamp}.txt"
            file_path = os.path.join(self.kb_path, filename)
            
            # 保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 添加到内存
            self.documents[filename] = content
            return filename
        
        elif file_type == 'pdf':
            # 对于PDF，我们保存为txt副本
            filename = f"{title}_{timestamp}.txt"
            file_path = os.path.join(self.kb_path, filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.documents[filename] = content
            return filename + " (从PDF导入)"
    
    def add_pdf_file(self, pdf_path):
        """直接添加PDF文件（不复制内容）"""
        if not os.path.exists(pdf_path):
            return None, "文件不存在"
        
        filename = os.path.basename(pdf_path)
        content = self._read_pdf(pdf_path)
        
        if content:
            # 保存为txt副本
            txt_filename = filename.replace('.pdf', '.txt')
            txt_path = os.path.join(self.kb_path, txt_filename)
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.documents[txt_filename] = content
            return txt_filename, f"已导入PDF: {filename}"
        
        return None, "PDF读取失败"
    
    def search(self, query, top_k=3):
        """搜索相关内容"""
        results = []
        query_words = set(query.lower().split())
        
        for filename, content in self.documents.items():
            # 计算匹配分数
            content_lower = content.lower()
            score = 0
            for word in query_words:
                if len(word) > 1:  # 忽略单字
                    score += content_lower.count(word)
            
            if score > 0:
                # 提取相关片段
                first_word = next((w for w in query_words if w in content_lower), None)
                if first_word:
                    pos = content_lower.find(first_word)
                    start = max(0, pos - 100)
                    end = min(len(content), pos + 300)
                    snippet = content[start:end]
                else:
                    snippet = content[:200]
                
                results.append({
                    'filename': filename,
                    'score': score,
                    'snippet': snippet
                })
        
        # 按分数排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def list_documents(self):
        """列出所有文档"""
        return list(self.documents.keys())

class InsuranceAgentWithKB:
    """带知识库的保险代理人助手（支持PDF）"""
    
    def __init__(self, agent_name="我的助手"):
        self.agent_name = agent_name
        self.kb = InsuranceKnowledgeBase()
        self.conversation_history = []
        self.style = "professional"
        self.use_kb = True
        
        # 风格提示词
        self.style_prompts = {
            "professional": "你是一位资深的保险专家，请用专业、严谨的语言回答问题，适当使用专业术语。",
            "simple": "你是一位擅长用大白话解释保险的代理人，请用通俗易懂的语言回答，多用生活化的比喻。",
            "empathic": "你是一位非常贴心、善于共情的保险顾问，请用温暖、关怀的语气回答，先理解客户的担忧。"
        }
    
    def set_style(self, style):
        if style in self.style_prompts:
            self.style = style
            return f"已切换到【{style}】风格"
        return "风格不存在"
    
    def toggle_kb(self):
        self.use_kb = not self.use_kb
        status = "开启" if self.use_kb else "关闭"
        return f"知识库功能已{status}"
    
    def add_to_kb(self, title, content):
        filename = self.kb.add_document(title, content)
        return f"已添加文档: {filename}"
    
    def import_pdf(self, pdf_path):
        """导入PDF文件"""
        filename, message = self.kb.add_pdf_file(pdf_path)
        return message
    
    def chat(self, user_input):
        messages = []
        system_prompt = self.style_prompts[self.style]
        
        # 如果开启知识库，先搜索相关内容
        if self.use_kb:
            search_results = self.kb.search(user_input)
            if search_results:
                kb_context = "\n\n请基于以下参考资料回答问题：\n"
                for i, result in enumerate(search_results, 1):
                    kb_context += f"\n【参考资料{i}】{result['snippet']}\n"
                system_prompt += kb_context
        
        messages.append({"role": "system", "content": system_prompt})
        
        # 添加历史记录
        for msg in self.conversation_history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=messages,
                temperature=0.8,
                max_tokens=1000
            )
            
            ai_reply = response.choices[0].message.content
            
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": ai_reply})
            
            return ai_reply
            
        except Exception as e:
            return f"出错了：{e}"
    
    def show_status(self):
        status = f"""
当前状态：
• 当前风格：{self.style}
• 知识库状态：{'开启' if self.use_kb else '关闭'}
• 知识库文档数：{len(self.kb.documents)}
• 对话历史轮数：{len(self.conversation_history)//2}
        """
        return status

def main():
    print("=" * 60)
    print("      保险代理人智能助手 v0.5 - PDF增强版")
    print("=" * 60)
    print("✨ 新功能：")
    print("  • 支持PDF文件直接导入")
    print("  • 自动读取PDF内容并建立知识库")
    print("  • 可随时开关知识库，对比效果")
    print("-" * 60)
    
    agent = InsuranceAgentWithKB()
    
    print("\n🛠️ 可用命令：")
    print("  /style 专业版   - 切换风格")
    print("  /kb            - 开关知识库")
    print("  /add           - 添加新知识")
    print("  /pdf 文件路径   - 导入PDF文件")
    print("  /list          - 列出所有文档")
    print("  /status        - 显示当前状态")
    print("  /clear         - 清空对话")
    print("  /quit 或 q     - 退出")
    print("-" * 60)
    
    while True:
        print("\n" + "-" * 60)
        user_input = input("你：").strip()
        
        if user_input.lower() in ['/quit', 'q']:
            print("感谢使用，再见！")
            break
        
        if user_input.startswith('/'):
            cmd = user_input.lower()
            
            if cmd == '/kb':
                print(agent.toggle_kb())
            
            elif cmd == '/list':
                docs = agent.kb.list_documents()
                if docs:
                    print("📚 知识库文档：")
                    for doc in docs:
                        print(f"  • {doc}")
                else:
                    print("知识库暂无文档")
            
            elif cmd == '/status':
                print(agent.show_status())
            
            elif cmd == '/clear':
                agent.conversation_history = []
                print("对话历史已清空")
            
            elif cmd.startswith('/style'):
                style_name = user_input[7:].strip()
                if style_name == "专业版":
                    print(agent.set_style("professional"))
                elif style_name == "通俗版":
                    print(agent.set_style("simple"))
                elif style_name == "共情版":
                    print(agent.set_style("empathic"))
                else:
                    print("请输入：专业版 / 通俗版 / 共情版")
            
            elif cmd.startswith('/add'):
                print("请输入标题：")
                title = input("标题：").strip()
                print("请输入内容（可多行，输入空行结束）：")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                content = "\n".join(lines)
                print(agent.add_to_kb(title, content))
            
            elif cmd.startswith('/pdf'):
                pdf_path = user_input[5:].strip()  # 去掉'/pdf '
                if os.path.exists(pdf_path):
                    print(f"正在导入PDF: {pdf_path}")
                    print(agent.import_pdf(pdf_path))
                else:
                    print(f"文件不存在: {pdf_path}")
            
            continue
        
        if not user_input:
            continue
        
        print("\n🤖 助手正在思考...")
        reply = agent.chat(user_input)
        print(f"\n🤖 助手：{reply}")

if __name__ == "__main__":
    main()