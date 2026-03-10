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

class ProposalGenerator:
    """保险计划书生成器"""
    
    def __init__(self):
        self.proposals = []
        self.templates = {
            "standard": "标准计划书",
            "simple": "简易版计划书",
            "detailed": "详细版计划书"
        }
    
    def generate_proposal(self, client_info, products, requirements=""):
        """
        生成保险计划书
        
        参数：
        - client_info: 客户信息字典
        - products: 推荐的产品列表
        - requirements: 特殊要求
        """
        
        # 构建客户信息文本
        client_text = "\n".join([f"{k}：{v}" for k, v in client_info.items()])
        
        # 构建产品信息文本
        products_text = "\n".join([f"- {p}" for p in products])
        
        prompt = f"""
你是一位专业的保险规划师。请根据以下客户信息和推荐产品，生成一份专业的保险计划书。

【客户信息】
{client_text}

【推荐产品】
{products_text}

【特殊要求】
{requirements if requirements else "无"}

请按照以下格式生成计划书：

==================== 保险计划书 ====================

一、客户需求分析
（分析客户的年龄、家庭状况、经济情况等，说明为什么需要这些保障）

二、方案设计思路
（解释为什么推荐这些产品，如何搭配）

三、产品详细说明
（每个产品的保障内容、保额、保费、缴费期等）

四、保障利益演示
（用表格形式展示不同情况下的理赔金额）

| 保障项目 | 保额 | 理赔条件 | 理赔金额 |
|---------|------|---------|---------|
| 重疾保障 | 50万 | 确诊重疾 | 50万 |
| 医疗保障 | 200万 | 住院医疗 | 实报实销 |

五、保费明细
（总保费、缴费方式、缴费年限）

六、投保建议
（注意事项、健康告知提醒等）

================================================
"""
        
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位资深的保险规划师，擅长为客户量身定制保险计划书。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=2500
            )
            
            proposal = response.choices[0].message.content
            
            # 保存到历史
            self.proposals.append({
                "client_info": client_info,
                "products": products,
                "proposal": proposal,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return proposal
            
        except Exception as e:
            return f"计划书生成失败：{e}"
    
    def generate_simple_proposal(self, client_name, age, budget, needs):
        """
        快速生成简易计划书
        """
        prompt = f"""
请为以下客户生成一份简易保险计划书：

客户姓名：{client_name}
年龄：{age}
预算：{budget}元/年
主要需求：{needs}

要求：
1. 推荐2-3款适合的产品组合
2. 说明每个产品的保障作用和预估保费
3. 总保费控制在预算内
4. 用简洁易懂的语言
"""
        
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位贴心的保险顾问，擅长用简单的话给客户介绍保险方案。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"简易计划书生成失败：{e}"
    
    def save_proposal(self, index=-1, filename=None):
        """保存计划书到文件"""
        if not self.proposals:
            return "暂无计划书历史"
        
        if index == -1:
            proposal_item = self.proposals[-1]  # 默认最新
        else:
            if index < 0 or index >= len(self.proposals):
                return "索引超出范围"
            proposal_item = self.proposals[index]
        
        if not filename:
            client_name = proposal_item["client_info"].get("姓名", "客户")
            filename = f"计划书_{client_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write(f"生成时间：{proposal_item['time']}\n")
            f.write("=" * 60 + "\n\n")
            f.write(proposal_item['proposal'])
        
        return f"计划书已保存到 {filename}"
    
    def list_proposals(self):
        """列出所有计划书历史"""
        if not self.proposals:
            return []
        
        return [{
            "index": i,
            "client": p["client_info"].get("姓名", "未知"),
            "time": p["time"]
        } for i, p in enumerate(self.proposals)]

def main():
    print("=" * 60)
    print("      保险计划书智能生成器 v1.0")
    print("=" * 60)
    print("✨ 功能：")
    print("  • 详细计划书（完整版）")
    print("  • 简易计划书（快速版）")
    print("  • 保存/查看历史")
    print("-" * 60)
    
    generator = ProposalGenerator()
    
    while True:
        print("\n" + "-" * 60)
        print("请选择模式：")
        print("1. 生成详细计划书")
        print("2. 生成简易计划书（快速）")
        print("3. 查看/保存历史")
        print("4. 退出")
        print("-" * 30)
        
        choice = input("请输入数字（1-4）：").strip()
        
        if choice == '1':
            print("\n📌 详细计划书模式")
            print("请输入客户信息：")
            
            client_info = {}
            client_info["姓名"] = input("客户姓名：").strip()
            client_info["年龄"] = input("年龄：").strip()
            client_info["性别"] = input("性别：").strip()
            client_info["职业"] = input("职业：").strip()
            client_info["婚姻状况"] = input("婚姻状况：").strip()
            client_info["子女情况"] = input("子女情况：").strip()
            client_info["年收入"] = input("年收入（万）：").strip()
            client_info["预算"] = input("预算（元/年）：").strip()
            
            print("\n请输入推荐产品（每行一个，输入空行结束）：")
            products = []
            while True:
                product = input()
                if product == "":
                    break
                products.append(product)
            
            requirements = input("\n是否有特殊要求？（直接回车跳过）：").strip()
            
            if not products:
                print("❌ 至少需要一个产品")
                continue
            
            print("\n🤖 正在生成计划书...")
            proposal = generator.generate_proposal(client_info, products, requirements)
            print("\n" + "=" * 60)
            print(proposal)
            print("=" * 60)
            
            save = input("\n是否保存这份计划书？(y/n)：").strip().lower()
            if save == 'y':
                print(generator.save_proposal())
        
        elif choice == '2':
            print("\n📌 简易计划书模式")
            name = input("客户姓名：").strip()
            age = input("年龄：").strip()
            budget = input("预算（元/年）：").strip()
            needs = input("主要需求（如：重疾、医疗、教育金）：").strip()
            
            print("\n🤖 正在生成简易计划书...")
            proposal = generator.generate_simple_proposal(name, age, budget, needs)
            print("\n" + "=" * 60)
            print(proposal)
            print("=" * 60)
        
        elif choice == '3':
            history = generator.list_proposals()
            if not history:
                print("📭 暂无计划书历史")
            else:
                print("\n📚 计划书历史：")
                for item in history:
                    print(f"{item['index']}. {item['client']} - {item['time']}")
                
                idx = input("\n输入序号查看详细（直接回车返回）：").strip()
                if idx.isdigit():
                    idx = int(idx)
                    if 0 <= idx < len(history):
                        print("\n" + generator.proposals[idx]['proposal'])
                        save = input("\n是否保存这份计划书？(y/n)：").strip().lower()
                        if save == 'y':
                            print(generator.save_proposal(idx))
        
        elif choice == '4':
            print("感谢使用，再见！")
            break
        
        else:
            print("❌ 无效选择，请输入1-4")

if __name__ == "__main__":
    main()