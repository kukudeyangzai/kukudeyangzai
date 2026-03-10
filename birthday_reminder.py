# 客户生日提醒助手
import os
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("ARK_API_KEY")
endpoint_id = os.getenv("ENDPOINT_ID")

client = OpenAI(
    api_key=api_key,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

class BirthdayReminder:
    def __init__(self, db_path="customers.db"):
        self.db_path = db_path
    
    def get_upcoming_birthdays(self, days=7):
        """获取即将过生日的客户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 假设customers表有birthday字段
        cursor.execute('''
            SELECT id, name, phone, birthday, notes 
            FROM customers 
            WHERE birthday IS NOT NULL
        ''')
        
        customers = cursor.fetchall()
        conn.close()
        
        upcoming = []
        today = datetime.now()
        
        for c in customers:
            # 解析生日
            try:
                bday = datetime.strptime(c[3], "%Y-%m-%d")
                # 计算今年生日
                this_year_bday = bday.replace(year=today.year)
                days_until = (this_year_bday - today).days
                
                if 0 <= days_until <= days:
                    upcoming.append({
                        'id': c[0],
                        'name': c[1],
                        'phone': c[2],
                        'birthday': c[3],
                        'days_until': days_until,
                        'notes': c[4]
                    })
            except:
                continue
        
        return sorted(upcoming, key=lambda x: x['days_until'])
    
    def generate_birthday_message(self, customer_name, days_left, style="温暖"):
        """生成生日祝福文案"""
        prompt = f"""
客户姓名：{customer_name}
距离生日：{days_left}天
风格：{style}

请生成一段生日祝福文案，要求：
1. 包含保险人的职业特色
2. 自然植入健康/保障理念
3. 不直接推销产品
4. 可附带小礼物建议
5. {days_left}天后发送
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位贴心的保险代理人，擅长维系客户关系。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"生成失败：{e}"
    
    def generate_gift_suggestion(self, age, gender, relation):
        """推荐生日礼物"""
        prompt = f"""
客户年龄：{age}
客户性别：{gender}
客户关系：{relation}
预算范围：200-500元

请推荐一份合适的生日礼物，要求：
1. 实用且有心意
2. 可与保险理念结合
3. 给出推荐理由
"""
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位送礼专家，擅长挑选贴心礼物。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"推荐失败：{e}"

def main():
    print("=" * 60)
    print("      客户生日提醒助手 v1.0")
    print("=" * 60)
    
    br = BirthdayReminder()
    
    while True:
        print("\n1. 查看近期生日客户")
        print("2. 生成生日祝福")
        print("3. 推荐生日礼物")
        print("4. 退出")
        
        choice = input("\n请选择：").strip()
        
        if choice == '1':
            days = input("提前几天提醒（默认7天）：").strip()
            days = int(days) if days else 7
            upcoming = br.get_upcoming_birthdays(days)
            
            if upcoming:
                print(f"\n🎂 未来{days}天内过生日的客户：")
                for c in upcoming:
                    print(f"{c['name']} | {c['phone']} | {c['birthday']} | {c['days_until']}天后")
            else:
                print("📭 暂无近期过生日的客户")
        
        elif choice == '2':
            name = input("客户姓名：").strip()
            days = input("距离生日天数：").strip()
            style = input("风格（温暖/正式/幽默，默认温暖）：").strip() or "温暖"
            print("\n💌 祝福文案：")
            print(br.generate_birthday_message(name, days, style))
        
        elif choice == '3':
            age = input("客户年龄：").strip()
            gender = input("客户性别：").strip()
            relation = input("与客户关系：").strip()
            print("\n🎁 礼物推荐：")
            print(br.generate_gift_suggestion(age, gender, relation))
        
        elif choice == '4':
            break

if __name__ == "__main__":
    main()