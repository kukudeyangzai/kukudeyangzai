# AI陪练助手 - 模拟客户对话
import os
import random
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("ARK_API_KEY")
endpoint_id = os.getenv("ENDPOINT_ID")

client = OpenAI(
    api_key=api_key,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

class AITraining:
    def __init__(self):
        self.client_types = {
            "谨慎型": "对保险有疑虑，需要详细解释，容易拒绝",
            "爽快型": "信任代理人，决策快，但可能要求优惠",
            "比较型": "会对比多家产品，要求性价比",
            "跟风型": "看别人买才想买，容易动摇",
            "专业型": "自己研究过保险，会问专业问题"
        }
        
        self.scenarios = [
            "第一次接触保险",
            "有既往病史",
            "预算有限",
            "想给孩子买",
            "给父母买",
            "已经有保单想加保",
            "理赔被拒过",
            "朋友推荐来的"
        ]
    
    def start_training(self, client_type, scenario, difficulty="中等"):
        """开始模拟训练"""
        prompt = f"""
你现在扮演一位{client_type}客户。
场景：{scenario}
难度：{difficulty}

客户特点：{self.client_types.get(client_type, '普通客户')}

请开始和保险代理人对话。你会：
1. 提出真实客户可能问的问题
2. 表现出该类型客户的典型反应
3. 根据代理人的回答调整态度
4. 会提出异议和顾虑

现在，客户说："你好，我想了解一下保险"
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": f"你是一位{client_type}的客户，正在进行保险咨询。"},
                    {"role": "assistant", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"训练启动失败：{e}"
    
    def generate_questions(self, client_type, product):
        """生成客户可能问的问题"""
        prompt = f"""
客户类型：{client_type}
咨询产品：{product}

请生成10个这类客户最可能问的问题：
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位经验丰富的保险培训师。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"生成失败：{e}"
    
    def evaluate_response(self, question, your_response):
        """评估你的回答"""
        prompt = f"""
客户问题：{question}
你的回答：{your_response}

请评估：
1. 回答的专业性（1-10分）
2. 回答的亲和力（1-10分）
3. 异议处理效果（1-10分）
4. 优点分析
5. 改进建议
6. 更好的回答示范
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位严格的销售教练。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"评估失败：{e}"
    
    def handle_objection(self, objection):
        """处理异议话术"""
        prompt = f"""
客户异议：{objection}

请提供：
1. 理解客户顾虑
2. 3种不同风格的话术回应
3. 可以使用的案例
4. 避坑指南
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是异议处理专家，擅长化解客户疑虑。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"生成失败：{e}"

def main():
    print("=" * 60)
    print("      AI陪练助手 v1.0")
    print("=" * 60)
    
    trainer = AITraining()
    
    while True:
        print("\n1. 开始模拟对话")
        print("2. 常见问题练习")
        print("3. 评估你的回答")
        print("4. 异议处理练习")
        print("5. 退出")
        
        choice = input("\n请选择：").strip()
        
        if choice == '1':
            print("\n客户类型：")
            for i, t in enumerate(trainer.client_types.keys(), 1):
                print(f"{i}. {t}")
            t_choice = int(input("请选择：").strip()) - 1
            client_type = list(trainer.client_types.keys())[t_choice]
            
            print("\n场景：")
            for i, s in enumerate(trainer.scenarios, 1):
                print(f"{i}. {s}")
            s_choice = int(input("请选择：").strip()) - 1
            scenario = trainer.scenarios[s_choice]
            
            print("\n🤖 开始对话...")
            print(trainer.start_training(client_type, scenario))
        
        elif choice == '2':
            c_type = input("客户类型：").strip()
            product = input("咨询产品：").strip()
            print("\n📋 常见问题：")
            print(trainer.generate_questions(c_type, product))
        
        elif choice == '3':
            q = input("客户问题：").strip()
            r = input("你的回答：").strip()
            print("\n📊 评估结果：")
            print(trainer.evaluate_response(q, r))
        
        elif choice == '4':
            obj = input("客户异议：").strip()
            print("\n💡 应对话术：")
            print(trainer.handle_objection(obj))
        
        elif choice == '5':
            break

if __name__ == "__main__":
    main()