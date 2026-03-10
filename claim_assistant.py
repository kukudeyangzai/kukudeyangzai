# 理赔智能助手 - 基础版本
import os
import json
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

class ClaimAssistant:
    def __init__(self):
        self.claim_types = ["重疾险", "医疗险", "意外险", "寿险"]
        self.claim_status = ["资料准备", "已提交", "审核中", "补充材料", "理赔中", "已完成", "拒赔"]
    
    def analyze_claim(self, diagnosis, policy_type):
        """分析理赔可能性和注意事项"""
        prompt = f"""
客户诊断：{diagnosis}
保险类型：{policy_type}

请分析：
1. 是否符合理赔条件
2. 需要准备哪些材料
3. 理赔流程和时间预估
4. 可能的拒赔风险点
5. 给代理人的建议
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位资深的理赔顾问，精通各类保险理赔。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"分析失败：{e}"
    
    def get_document_list(self, claim_type, disease=None):
        """获取理赔所需材料清单"""
        prompt = f"""
理赔类型：{claim_type}
疾病/情况：{disease if disease else '通用'}

请列出理赔所需的所有材料清单，包括：
1. 身份证明类
2. 医疗证明类
3. 费用凭证类
4. 其他特殊材料
5. 注意事项
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位理赔专家，熟悉各家保险公司的理赔要求。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"获取清单失败：{e}"
    
    def check_documents(self, documents):
        """检查材料是否齐全"""
        prompt = f"""
请检查以下理赔材料是否齐全，并指出缺失或需要补充的材料：

{documents}

请输出：
1. 齐全度评估
2. 缺失材料清单
3. 每份材料的注意事项
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位细心的理赔审核员。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"检查失败：{e}"
    
    def simulate_claim(self, policy_type, disease, amount):
        """模拟理赔审核"""
        prompt = f"""
保险类型：{policy_type}
疾病诊断：{disease}
申请金额：{amount}元

请模拟理赔审核流程：
1. 初步审核结果
2. 可能的问题点
3. 需要补充的材料
4. 预估赔付比例
5. 理赔时间线
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位保险公司理赔审核员，严格但不失温度。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"模拟失败：{e}"
    
    def handle_rejection(self, policy_type, disease, reason):
        """处理拒赔情况"""
        prompt = f"""
保险类型：{policy_type}
疾病诊断：{disease}
拒赔理由：{reason}

请给出应对建议：
1. 拒赔是否合理
2. 如何与客户沟通
3. 申诉的可能性
4. 需要补充的证据
5. 备选方案
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位经验丰富的理赔纠纷处理专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"处理建议失败：{e}"

def main():
    print("=" * 60)
    print("      理赔智能助手 v1.0")
    print("=" * 60)
    print("功能：")
    print("1. 理赔条件分析")
    print("2. 材料清单生成")
    print("3. 材料完整性检查")
    print("4. 理赔模拟审核")
    print("5. 拒赔处理建议")
    print("-" * 60)
    
    ca = ClaimAssistant()
    
    while True:
        print("\n请选择：")
        print("1. 理赔分析")
        print("2. 材料清单")
        print("3. 检查材料")
        print("4. 模拟审核")
        print("5. 拒赔处理")
        print("6. 退出")
        
        choice = input("\n请输入数字：").strip()
        
        if choice == '1':
            diagnosis = input("请输入诊断结果：").strip()
            policy = input("保险类型（重疾险/医疗险/意外险/寿险）：").strip()
            print("\n🤖 分析中...")
            print(ca.analyze_claim(diagnosis, policy))
        
        elif choice == '2':
            claim_type = input("理赔类型：").strip()
            disease = input("疾病名称（直接回车跳过）：").strip()
            print("\n📋 材料清单：")
            print(ca.get_document_list(claim_type, disease if disease else None))
        
        elif choice == '3':
            print("请输入已有材料（每行一个，空行结束）：")
            docs = []
            while True:
                line = input()
                if line == "":
                    break
                docs.append(line)
            print("\n🔍 检查中...")
            print(ca.check_documents("\n".join(docs)))
        
        elif choice == '4':
            policy = input("保险类型：").strip()
            disease = input("疾病诊断：").strip()
            amount = input("申请金额：").strip()
            print("\n⚖️ 模拟审核中...")
            print(ca.simulate_claim(policy, disease, amount))
        
        elif choice == '5':
            policy = input("保险类型：").strip()
            disease = input("疾病诊断：").strip()
            reason = input("拒赔理由：").strip()
            print("\n💡 处理建议：")
            print(ca.handle_rejection(policy, disease, reason))
        
        elif choice == '6':
            print("感谢使用！")
            break

if __name__ == "__main__":
    main()