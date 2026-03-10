import os
import json
import sqlite3
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

class CustomerManager:
    """客户关系管理系统"""
    
    def __init__(self, db_path="customers.db"):
        self.db_path = db_path
        self.current_customer = None
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建客户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                age INTEGER,
                gender TEXT,
                occupation TEXT,
                income TEXT,
                family_status TEXT,
                source TEXT,
                status TEXT DEFAULT '潜在客户',
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                notes TEXT
            )
        ''')
        
        # 创建沟通记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                interaction_date TIMESTAMP,
                type TEXT,
                content TEXT,
                next_step TEXT,
                sentiment TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # 创建保险需求表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insurance_needs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                product_type TEXT,
                budget TEXT,
                priority INTEGER,
                status TEXT,
                notes TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ 数据库初始化完成")
    
    def add_customer(self, customer_info):
        """添加新客户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO customers (
                name, phone, age, gender, occupation, income, 
                family_status, source, status, created_at, updated_at, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            customer_info.get('name', ''),
            customer_info.get('phone', ''),
            customer_info.get('age', 0),
            customer_info.get('gender', ''),
            customer_info.get('occupation', ''),
            customer_info.get('income', ''),
            customer_info.get('family_status', ''),
            customer_info.get('source', ''),
            customer_info.get('status', '潜在客户'),
            now, now,
            customer_info.get('notes', '')
        ))
        
        customer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ 客户添加成功，ID: {customer_id}")
        return customer_id
    
    def search_customers(self, keyword):
        """搜索客户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, phone, age, status, created_at 
            FROM customers 
            WHERE name LIKE ? OR phone LIKE ? OR notes LIKE ?
            ORDER BY updated_at DESC
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_customer_detail(self, customer_id):
        """获取客户详细信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取基本信息
        cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        customer = cursor.fetchone()
        
        if not customer:
            conn.close()
            return None
        
        # 获取沟通记录
        cursor.execute('''
            SELECT * FROM interactions 
            WHERE customer_id = ? 
            ORDER BY interaction_date DESC
        ''', (customer_id,))
        interactions = cursor.fetchall()
        
        # 获取保险需求
        cursor.execute('SELECT * FROM insurance_needs WHERE customer_id = ?', (customer_id,))
        needs = cursor.fetchall()
        
        conn.close()
        
        return {
            'customer': customer,
            'interactions': interactions,
            'needs': needs
        }
    
    def add_interaction(self, customer_id, interaction_type, content, next_step=""):
        """添加沟通记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 简单的情感分析（调用AI）
        sentiment = self.analyze_sentiment(content)
        
        cursor.execute('''
            INSERT INTO interactions (
                customer_id, interaction_date, type, content, next_step, sentiment
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (customer_id, now, interaction_type, content, next_step, sentiment))
        
        # 更新客户更新时间
        cursor.execute('''
            UPDATE customers SET updated_at = ? WHERE id = ?
        ''', (now, customer_id))
        
        conn.commit()
        conn.close()
        
        print(f"✅ 沟通记录已添加")
    
    def analyze_sentiment(self, text):
        """分析客户情绪"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一个情绪分析专家。请分析以下文本的情绪倾向，只返回一个词：积极/中性/消极"},
                    {"role": "user", "content": text[:200]}  # 只分析前200字
                ],
                temperature=0.3,
                max_tokens=10
            )
            return response.choices[0].message.content.strip()
        except:
            return "中性"
    
    def add_insurance_need(self, customer_id, product_type, budget, priority, notes=""):
        """添加保险需求"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO insurance_needs (
                customer_id, product_type, budget, priority, status, notes
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (customer_id, product_type, budget, priority, '待跟进', notes))
        
        conn.commit()
        conn.close()
        print(f"✅ 保险需求已添加")
    
    def get_follow_up_list(self, days=7):
        """获取待跟进客户列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, c.name, c.phone, c.status, MAX(i.interaction_date) as last_contact
            FROM customers c
            LEFT JOIN interactions i ON c.id = i.customer_id
            GROUP BY c.id
            HAVING last_contact IS NULL OR julianday('now') - julianday(last_contact) > ?
            ORDER BY last_contact ASC
        ''', (days,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def ai_analyze_customer(self, customer_id):
        """用AI分析客户需求"""
        detail = self.get_customer_detail(customer_id)
        if not detail:
            return "客户不存在"
        
        customer = detail['customer']
        interactions = detail['interactions']
        
        # 构建提示词
        prompt = f"""
客户信息：
- 姓名：{customer[1]}
- 年龄：{customer[3]}
- 职业：{customer[5]}
- 收入：{customer[6]}
- 家庭情况：{customer[7]}
- 来源：{customer[8]}
- 状态：{customer[9]}

最近沟通记录：
"""
        for i in interactions[:3]:  # 最近3条
            prompt += f"- [{i[2]}] {i[3][:100]}...\n"
        
        prompt += """
请分析：
1. 客户的核心保险需求是什么？
2. 目前处于什么阶段？（了解/比较/决策/犹豫）
3. 下一步应该推荐什么产品？
4. 沟通中需要注意什么？
5. 成交可能性评估（高/中/低）

请给出专业建议。
"""
        
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位资深的保险销售顾问，擅长分析客户需求并提供跟进建议。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"分析失败：{e}"

def main():
    print("=" * 60)
    print("      保险代理人客户管理系统 v1.0")
    print("=" * 60)
    print("✨ 功能：")
    print("  • 客户信息管理（增删查改）")
    print("  • 沟通记录跟踪")
    print("  • 保险需求分析")
    print("  • AI智能分析客户")
    print("  • 待跟进提醒")
    print("-" * 60)
    
    cm = CustomerManager()
    
    while True:
        print("\n" + "-" * 60)
        print("请选择操作：")
        print("1. 添加新客户")
        print("2. 搜索客户")
        print("3. 查看客户详情")
        print("4. 添加沟通记录")
        print("5. 添加保险需求")
        print("6. AI分析客户")
        print("7. 待跟进列表")
        print("8. 退出")
        print("-" * 30)
        
        choice = input("请输入数字（1-8）：").strip()
        
        if choice == '1':
            print("\n📝 添加新客户")
            customer = {}
            customer['name'] = input("姓名：").strip()
            customer['phone'] = input("电话：").strip()
            customer['age'] = input("年龄：").strip()
            customer['gender'] = input("性别：").strip()
            customer['occupation'] = input("职业：").strip()
            customer['income'] = input("年收入范围：").strip()
            customer['family_status'] = input("家庭情况：").strip()
            customer['source'] = input("客户来源：").strip()
            customer['notes'] = input("备注：").strip()
            
            cm.add_customer(customer)
        
        elif choice == '2':
            keyword = input("输入搜索关键词（姓名/电话）：").strip()
            results = cm.search_customers(keyword)
            
            if results:
                print("\n📋 搜索结果：")
                for r in results:
                    print(f"ID: {r[0]}, 姓名: {r[1]}, 电话: {r[2]}, 年龄: {r[3]}, 状态: {r[4]}")
            else:
                print("未找到匹配的客户")
        
        elif choice == '3':
            cid = input("输入客户ID：").strip()
            detail = cm.get_customer_detail(cid)
            
            if detail:
                c = detail['customer']
                print("\n" + "=" * 50)
                print(f"客户ID：{c[0]}")
                print(f"姓名：{c[1]}")
                print(f"电话：{c[2]}")
                print(f"年龄：{c[3]}")
                print(f"性别：{c[4]}")
                print(f"职业：{c[5]}")
                print(f"收入：{c[6]}")
                print(f"家庭情况：{c[7]}")
                print(f"来源：{c[8]}")
                print(f"状态：{c[9]}")
                print(f"创建时间：{c[10]}")
                print(f"最后更新：{c[11]}")
                print(f"备注：{c[12]}")
                
                if detail['interactions']:
                    print("\n📞 最近沟通记录：")
                    for i in detail['interactions'][:5]:
                        print(f"  [{i[2]}] {i[3][:100]}...")
                
                if detail['needs']:
                    print("\n🛡️ 保险需求：")
                    for n in detail['needs']:
                        print(f"  {n[2]} | 预算:{n[3]} | 优先级:{n[4]} | 状态:{n[5]}")
            else:
                print("客户不存在")
        
        elif choice == '4':
            cid = input("客户ID：").strip()
            itype = input("沟通类型（电话/微信/面谈）：").strip()
            content = input("沟通内容：").strip()
            next_step = input("下一步计划：").strip()
            cm.add_interaction(cid, itype, content, next_step)
        
        elif choice == '5':
            cid = input("客户ID：").strip()
            ptype = input("产品类型（重疾/医疗/意外/养老/教育金）：").strip()
            budget = input("预算范围：").strip()
            priority = input("优先级（1-5，5最高）：").strip()
            notes = input("备注：").strip()
            cm.add_insurance_need(cid, ptype, budget, priority, notes)
        
        elif choice == '6':
            cid = input("客户ID：").strip()
            print("\n🤖 AI正在分析客户...")
            analysis = cm.ai_analyze_customer(cid)
            print("\n" + "=" * 50)
            print(analysis)
            print("=" * 50)
        
        elif choice == '7':
            days = input("多少天未跟进？（默认7天）：").strip()
            days = int(days) if days else 7
            followups = cm.get_follow_up_list(days)
            
            if followups:
                print(f"\n📅 超过{days}天未跟进的客户：")
                for f in followups:
                    last = f[4] if f[4] else "从未联系"
                    print(f"ID: {f[0]}, 姓名: {f[1]}, 电话: {f[2]}, 状态: {f[3]}, 最后联系: {last}")
            else:
                print("🎉 所有客户都已及时跟进！")
        
        elif choice == '8':
            print("感谢使用，再见！")
            break
        
        else:
            print("❌ 无效选择，请输入1-8")

if __name__ == "__main__":
    main()