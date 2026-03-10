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

class ProductComparator:
    """保险产品对比工具"""
    
    def __init__(self):
        self.compare_history = []
    
    def compare_products(self, product1, product2, details=""):
        """
        对比两款保险产品
        
        参数：
        - product1: 第一款产品名称/描述
        - product2: 第二款产品名称/描述
        - details: 额外对比要求（可选）
        """
        
        prompt = f"""
你是一位专业的保险产品分析师。请对以下两款保险产品进行详细对比，生成结构化的对比表格。

【产品一】：{product1}
【产品二】：{product2}

{details}

请按照以下维度进行对比（如果信息不足，注明“信息缺失”）：

1. 基本信息
   - 产品类型
   - 承保公司
   - 投保年龄
   - 保障期限
   - 缴费方式

2. 保障内容
   - 重疾保障（病种数量、赔付次数、赔付比例）
   - 中症保障（病种数量、赔付次数、赔付比例）
   - 轻症保障（病种数量、赔付次数、赔付比例）
   - 身故/全残保障
   - 豁免条款

3. 特色亮点
   - 产品特色
   - 额外保障
   - 增值服务

4. 价格对比
   - 不同年龄段的保费示例
   - 性价比分析

5. 适合人群
   - 产品优势
   - 适合哪类客户
   - 注意事项

请用表格形式呈现，格式如下：
| 对比维度 | 产品一 | 产品二 |
|---------|--------|--------|
| 维度1   | 内容   | 内容   |

最后给出专业的购买建议。
"""
        
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位资深的保险产品分析师，擅长用表格形式清晰对比产品。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,  # 降低温度，让回答更准确
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            
            # 保存对比历史
            self.compare_history.append({
                "product1": product1,
                "product2": product2,
                "result": result,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return result
            
        except Exception as e:
            return f"对比生成失败：{e}"
    
    def save_comparison(self, filename=None):
        """保存对比结果"""
        if not self.compare_history:
            return "暂无对比历史"
        
        if not filename:
            filename = f"product_compare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            for item in self.compare_history:
                f.write("=" * 60 + "\n")
                f.write(f"时间：{item['time']}\n")
                f.write(f"产品一：{item['product1']}\n")
                f.write(f"产品二：{item['product2']}\n")
                f.write("-" * 40 + "\n")
                f.write(item['result'])
                f.write("\n\n")
        
        return f"对比结果已保存到 {filename}"
    
    def quick_compare(self, products_info):
        """
        快速对比多个产品（用简单表格）
        products_info: 字典格式 {"产品名": "产品描述"}
        """
        if len(products_info) < 2:
            return "至少需要两个产品"
        
        product_names = list(products_info.keys())
        product_descs = list(products_info.values())
        
        prompt = f"请用表格形式快速对比以下{len(product_names)}款产品的主要特点：\n\n"
        for i, (name, desc) in enumerate(products_info.items(), 1):
            prompt += f"产品{i}【{name}】：{desc}\n"
        
        prompt += "\n请重点关注：保障范围、价格区间、适合人群的差异。"
        
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位保险产品专家，擅长快速抓住产品核心差异。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"快速对比失败：{e}"

def main():
    print("=" * 60)
    print("      保险产品智能对比工具 v1.0")
    print("=" * 60)
    print("✨ 功能：")
    print("  • 详细对比两款产品（表格形式）")
    print("  • 快速对比多个产品")
    print("  • 保存对比结果")
    print("-" * 60)
    
    comparator = ProductComparator()
    
    while True:
        print("\n" + "-" * 60)
        print("请选择模式：")
        print("1. 详细对比（两款产品）")
        print("2. 快速对比（多款产品）")
        print("3. 查看/保存历史")
        print("4. 退出")
        print("-" * 30)
        
        choice = input("请输入数字（1-4）：").strip()
        
        if choice == '1':
            print("\n📌 详细对比模式")
            p1 = input("请输入第一款产品名称/描述：").strip()
            p2 = input("请输入第二款产品名称/描述：").strip()
            details = input("是否有额外的对比要求？（直接回车跳过）：").strip()
            
            if not p1 or not p2:
                print("❌ 产品信息不能为空")
                continue
            
            print("\n🤖 正在生成对比分析...")
            result = comparator.compare_products(p1, p2, details)
            print("\n" + "=" * 60)
            print(result)
            print("=" * 60)
            
            # 询问是否保存
            save = input("\n是否保存本次对比？(y/n)：").strip().lower()
            if save == 'y':
                print(comparator.save_comparison())
        
        elif choice == '2':
            print("\n📌 快速对比模式（至少2款，最多5款）")
            products = {}
            count = int(input("要对比几款产品？（2-5）：").strip())
            
            for i in range(count):
                name = input(f"产品{i+1}名称：").strip()
                desc = input(f"产品{i+1}简要描述：").strip()
                products[name] = desc
            
            print("\n🤖 正在生成快速对比...")
            result = comparator.quick_compare(products)
            print("\n" + "=" * 60)
            print(result)
            print("=" * 60)
        
        elif choice == '3':
            if not comparator.compare_history:
                print("📭 暂无对比历史")
            else:
                print(f"\n📚 共有 {len(comparator.compare_history)} 次对比记录")
                for i, item in enumerate(comparator.compare_history, 1):
                    print(f"{i}. [{item['time']}] {item['product1']} vs {item['product2']}")
                
                save = input("\n是否保存所有历史记录？(y/n)：").strip().lower()
                if save == 'y':
                    print(comparator.save_comparison())
        
        elif choice == '4':
            print("感谢使用，再见！")
            break
        
        else:
            print("❌ 无效选择，请输入1-4")

if __name__ == "__main__":
    main()