# 保单体检助手
import os
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

class PolicyCheck:
    def __init__(self):
        self.coverage_types = ["重疾险", "医疗险", "意外险", "寿险", "年金险"]
    
    def analyze_policies(self, policies):
        """分析现有保单"""
        prompt = f"""
请分析以下客户的现有保单：

{policies}

请从以下维度分析：
1. 保障完整性（缺少哪些保障）
2. 保额合理性（是否足够）
3. 保费压力（是否在合理范围）
4. 重复保障（哪些可以优化）
5. 缺口分析（需要补充什么）
6. 优化建议
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位专业的保单体检分析师。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"分析失败：{e}"
    
    def calculate_coverage_gap(self, age, income, debt, dependents):
        """计算保障缺口"""
        prompt = f"""
客户年龄：{age}
年收入：{income}万
负债：{debt}万
抚养人数：{dependents}

请计算：
1. 寿险保障缺口
2. 重疾险保障缺口
3. 医疗险需求
4. 意外险需求
5. 总保费建议
6. 分项配置建议
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位精算师，擅长计算保障需求。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"计算失败：{e}"
    
    def generate_report(self, customer_info, analysis_result):
        """生成保单体检报告"""
        prompt = f"""
客户信息：{customer_info}
分析结果：{analysis_result}

请生成一份专业的保单体检报告，包含：
1. 报告摘要
2. 现有保障分析
3. 保障缺口
4. 优化建议
5. 优先顺序
6. 注意事项
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位保险顾问，擅长撰写专业报告。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"生成失败：{e}"

def main():
    print("=" * 60)
    print("      保单体检助手 v1.0")
    print("=" * 60)
    
    pc = PolicyCheck()
    
    while True:
        print("\n1. 保单全面分析")
        print("2. 保障缺口计算")
        print("3. 生成体检报告")
        print("4. 退出")
        
        choice = input("\n请选择：").strip()
        
        if choice == '1':
            print("请输入现有保单（每行一个，空行结束）：")
            policies = []
            while True:
                line = input()
                if line == "":
                    break
                policies.append(line)
            print("\n🔍 分析中...")
            print(pc.analyze_policies("\n".join(policies)))
        
        elif choice == '2':
            age = input("年龄：").strip()
            income = input("年收入（万）：").strip()
            debt = input("负债（万）：").strip()
            dependents = input("抚养人数：").strip()
            print("\n📊 计算中...")
            print(pc.calculate_coverage_gap(age, income, debt, dependents))
        
        elif choice == '3':
            info = input("客户信息：").strip()
            analysis = input("分析结果：").strip()
            print("\n📄 生成报告中...")
            print(pc.generate_report(info, analysis))
        
        elif choice == '4':
            break

if __name__ == "__main__":
    main()