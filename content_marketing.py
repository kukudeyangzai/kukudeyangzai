import os
import json
from datetime import datetime, timedelta
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

class ContentMarketing:
    """内容营销助手 - 自动生成营销文案"""
    
    def __init__(self):
        self.content_history = []
        self.content_calendar = []
        
        # 内容主题模板
        self.topics = {
            "保险科普": [
                "重疾险和医疗险有什么区别？",
                "有了社保还要买商业保险吗？",
                "孩子的保险怎么买最划算？",
                "老年人还能买什么保险？",
                "保险理赔的流程是怎样的？"
            ],
            "产品解读": [
                "深度解析XX重疾险的优缺点",
                "XX医疗险真的值得买吗？",
                "对比三款热门意外险",
                "年金险适合什么人买？",
                "增额终身寿险的隐藏功能"
            ],
            "理赔案例": [
                "XX客户甲状腺癌获赔50万",
                "意外险理赔实录：摔伤也能赔",
                "医疗险理赔：住院花了10万赔了9.9万",
                "重疾险拒赔案例分析",
                "理赔时最容易忽略的细节"
            ],
            "行业动态": [
                "保险新规对消费者的影响",
                "2025年保险行业趋势",
                "保险公司评级怎么看？",
                "预定利率下调意味着什么？",
                "医保改革最新解读"
            ],
            "生活感悟": [
                "30岁后为什么要买保险？",
                "我为什么劝朋友买保险",
                "见过太多理赔，才懂保险的意义",
                "给新晋父母的建议：先保大人再保孩子",
                "一场大病让我明白的事"
            ]
        }
        
        # 平台风格
        self.platform_styles = {
            "朋友圈": "简短精炼，带emoji，有温度，配图建议，150字以内",
            "公众号": "专业深入，结构清晰，2000字左右，要有标题和小标题",
            "小红书": "种草风格，带话题标签，图文并茂，800字左右",
            "抖音脚本": "口语化，有开场白和结尾，带互动引导，500字以内",
            "知乎回答": "专业严谨，有数据支撑，分点论述，1000字左右",
            "视频号文案": "有故事性，情感共鸣，带行动号召，800字以内"
        }
    
    def generate_content(self, topic, platform="朋友圈", style="通俗", keywords=""):
        """
        生成营销内容
        
        参数：
        - topic: 内容主题
        - platform: 发布平台
        - style: 风格（通俗/专业/情感）
        - keywords: 关键词
        """
        
        prompt = f"""
你是一位资深的保险领域内容创作者。请根据以下要求生成一篇营销文案。

【主题】：{topic}
【发布平台】：{platform}
【平台风格】：{self.platform_styles.get(platform, "通俗易懂")}
【写作风格】：{style}
【关键词】：{keywords if keywords else "无"}

要求：
1. 标题要吸引人
2. 开头要有钩子，能抓住读者注意力
3. 内容要有价值，避免纯广告
4. 结尾要有互动或行动号召
5. 符合平台调性

请直接输出完整的文案。
"""
        
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位资深的保险内容营销专家，擅长写出高转化的文案。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            # 保存到历史
            self.content_history.append({
                "topic": topic,
                "platform": platform,
                "style": style,
                "content": content,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return content
            
        except Exception as e:
            return f"内容生成失败：{e}"
    
    def generate_article_series(self, main_topic, count=5):
        """
        生成系列文章
        """
        prompt = f"""
请围绕【{main_topic}】这个主题，规划一个由{count}篇文章组成的系列内容。

要求：
1. 每篇文章有独立的标题和切入点
2. 文章之间要有逻辑递进关系
3. 覆盖用户可能关心的不同角度
4. 用表格形式呈现

格式：
| 序号 | 文章标题 | 核心观点 | 适合人群 |
|-----|---------|---------|---------|
| 1 | ... | ... | ... |
"""
        
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位资深的内容策划专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"系列规划失败：{e}"
    
    def generate_daily_post(self, days=7):
        """
        生成一周的朋友圈内容
        """
        prompt = f"""
请为我规划接下来{days}天的保险朋友圈内容。

要求：
1. 每天一个主题，不重复
2. 包含：日期建议、文案、配图建议
3. 有科普、有案例、有感悟、有互动
4. 风格轻松亲切，带emoji
5. 每天不超过150字

请用表格形式输出：
| 日期 | 主题 | 文案 | 配图建议 |
|-----|-----|------|---------|
"""
        
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位朋友圈运营高手，擅长用短文案打动人心。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1500
            )
            
            calendar = response.choices[0].message.content
            self.content_calendar = calendar
            return calendar
            
        except Exception as e:
            return f"朋友圈规划失败：{e}"
    
    def generate_response(self, question, platform="知乎"):
        """
        生成问答平台的回答
        """
        prompt = f"""
请在【{platform}】上回答以下问题：

问题：{question}

要求：
1. 回答要专业、有说服力
2. 可以适当植入保险理念，但不要硬广告
3. 用数据和案例支撑观点
4. 结尾可以引导私信咨询
5. 符合平台调性
"""
        
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位在知乎、小红书等平台有影响力的保险博主。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"回答生成失败：{e}"
    
    def generate_video_script(self, topic, duration="60秒"):
        """
        生成短视频脚本
        """
        prompt = f"""
请为一条{duration}的短视频创作脚本，主题是：{topic}

要求：
1. 开头3秒要抓人
2. 中间有干货，有案例
3. 结尾有引导（点赞、关注、咨询）
4. 标注镜头建议和语气提示
5. 口语化，像在跟朋友聊天

格式：
【标题】：
【时长】：
【BGM建议】：

【0-5秒】画面：... 台词：...
【5-15秒】画面：... 台词：...
...
"""
        
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位爆款短视频编剧，擅长用短时间讲清保险知识。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"脚本生成失败：{e}"
    
    def repurpose_content(self, original_content, target_platforms):
        """
        将一篇内容改写成多个平台版本
        """
        platforms_str = "、".join(target_platforms)
        
        prompt = f"""
请将以下内容改写成适用于【{platforms_str}】的版本。

原文：
{original_content[:500]}...

要求：
1. 保持核心信息不变
2. 根据不同平台调性调整表达方式
3. 每个平台一个版本
4. 标注各平台的改写要点

请按平台分别输出。
"""
        
        try:
            response = client.chat.completions.create(
                model=endpoint_id,
                messages=[
                    {"role": "system", "content": "你是一位多平台内容运营专家，擅长一鱼多吃。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"改写失败：{e}"
    
    def save_content(self, index=-1, filename=None):
        """保存生成的内容"""
        if not self.content_history:
            return "暂无内容历史"
        
        if index == -1:
            item = self.content_history[-1]
        else:
            if index < 0 or index >= len(self.content_history):
                return "索引超出范围"
            item = self.content_history[index]
        
        if not filename:
            filename = f"营销文案_{item['platform']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write(f"主题：{item['topic']}\n")
            f.write(f"平台：{item['platform']}\n")
            f.write(f"风格：{item['style']}\n")
            f.write(f"生成时间：{item['time']}\n")
            f.write("=" * 60 + "\n\n")
            f.write(item['content'])
        
        return f"内容已保存到 {filename}"
    
    def list_history(self):
        """列出历史记录"""
        if not self.content_history:
            return []
        
        return [{
            "index": i,
            "topic": item['topic'][:30],
            "platform": item['platform'],
            "time": item['time']
        } for i, item in enumerate(self.content_history)]

def main():
    print("=" * 60)
    print("      保险内容营销助手 v1.0")
    print("=" * 60)
    print("✨ 功能：")
    print("  • 朋友圈文案生成")
    print("  • 公众号文章创作")
    print("  • 短视频脚本")
    print("  • 知乎/小红书回答")
    print("  • 一周内容规划")
    print("  • 一鱼多吃（多平台改写）")
    print("-" * 60)
    
    marketer = ContentMarketing()
    
    while True:
        print("\n" + "-" * 60)
        print("请选择模式：")
        print("1. 生成单篇文案")
        print("2. 规划一周朋友圈")
        print("3. 生成系列文章")
        print("4. 生成短视频脚本")
        print("5. 回答平台问题")
        print("6. 一鱼多吃（多平台改写）")
        print("7. 查看/保存历史")
        print("8. 退出")
        print("-" * 30)
        
        choice = input("请输入数字（1-8）：").strip()
        
        if choice == '1':
            print("\n📝 单篇文案生成")
            print("可选主题类别：")
            print("1. 保险科普  2. 产品解读  3. 理赔案例")
            print("4. 行业动态  5. 生活感悟  6. 自定义")
            
            topic_choice = input("请选择（1-6）：").strip()
            
            if topic_choice == '1':
                topics = marketer.topics["保险科普"]
                for i, t in enumerate(topics, 1):
                    print(f"{i}. {t}")
                idx = int(input("请选择主题编号：").strip()) - 1
                topic = topics[idx]
            elif topic_choice == '2':
                topics = marketer.topics["产品解读"]
                for i, t in enumerate(topics, 1):
                    print(f"{i}. {t}")
                idx = int(input("请选择主题编号：").strip()) - 1
                topic = topics[idx]
            elif topic_choice == '3':
                topics = marketer.topics["理赔案例"]
                for i, t in enumerate(topics, 1):
                    print(f"{i}. {t}")
                idx = int(input("请选择主题编号：").strip()) - 1
                topic = topics[idx]
            elif topic_choice == '4':
                topics = marketer.topics["行业动态"]
                for i, t in enumerate(topics, 1):
                    print(f"{i}. {t}")
                idx = int(input("请选择主题编号：").strip()) - 1
                topic = topics[idx]
            elif topic_choice == '5':
                topics = marketer.topics["生活感悟"]
                for i, t in enumerate(topics, 1):
                    print(f"{i}. {t}")
                idx = int(input("请选择主题编号：").strip()) - 1
                topic = topics[idx]
            else:
                topic = input("请输入自定义主题：").strip()
            
            print("\n选择平台：")
            platforms = list(marketer.platform_styles.keys())
            for i, p in enumerate(platforms, 1):
                print(f"{i}. {p}")
            p_idx = int(input("请选择（1-6）：").strip()) - 1
            platform = platforms[p_idx]
            
            style = input("风格（通俗/专业/情感，默认通俗）：").strip() or "通俗"
            keywords = input("关键词（可选）：").strip()
            
            print("\n🤖 正在生成文案...")
            content = marketer.generate_content(topic, platform, style, keywords)
            print("\n" + "=" * 60)
            print(content)
            print("=" * 60)
            
            save = input("\n是否保存？(y/n)：").strip().lower()
            if save == 'y':
                print(marketer.save_content())
        
        elif choice == '2':
            print("\n📅 一周朋友圈规划")
            days = input("规划几天？（默认7天）：").strip()
            days = int(days) if days else 7
            
            print("\n🤖 正在生成朋友圈规划...")
            calendar = marketer.generate_daily_post(days)
            print("\n" + "=" * 60)
            print(calendar)
            print("=" * 60)
        
        elif choice == '3':
            print("\n📚 系列文章规划")
            topic = input("请输入系列主题（如：重疾险选购指南）：").strip()
            count = input("规划几篇文章？（默认5篇）：").strip()
            count = int(count) if count else 5
            
            print("\n🤖 正在规划系列文章...")
            series = marketer.generate_article_series(topic, count)
            print("\n" + "=" * 60)
            print(series)
            print("=" * 60)
        
        elif choice == '4':
            print("\n🎬 短视频脚本生成")
            topic = input("视频主题：").strip()
            duration = input("视频时长（默认60秒）：").strip() or "60秒"
            
            print("\n🤖 正在生成脚本...")
            script = marketer.generate_video_script(topic, duration)
            print("\n" + "=" * 60)
            print(script)
            print("=" * 60)
        
        elif choice == '5':
            print("\n❓ 问答平台回答")
            question = input("请输入问题：").strip()
            print("\n选择平台：")
            print("1. 知乎  2. 小红书  3. 百度知道  4. 悟空问答")
            p_choice = input("请选择（1-4）：").strip()
            platforms = {"1": "知乎", "2": "小红书", "3": "百度知道", "4": "悟空问答"}
            platform = platforms.get(p_choice, "知乎")
            
            print("\n🤖 正在生成回答...")
            answer = marketer.generate_response(question, platform)
            print("\n" + "=" * 60)
            print(answer)
            print("=" * 60)
        
        elif choice == '6':
            print("\n🔄 一鱼多吃（多平台改写）")
            print("请粘贴原文（直接回车使用最新生成的内容）：")
            original = input().strip()
            
            if not original and marketer.content_history:
                original = marketer.content_history[-1]['content']
                print("使用最新生成的内容")
            elif not original:
                print("❌ 没有可用的原文")
                continue
            
            print("\n选择目标平台（可多选，用逗号分隔）：")
            platforms = list(marketer.platform_styles.keys())
            for i, p in enumerate(platforms, 1):
                print(f"{i}. {p}")
            choices = input("请输入编号（如：1,3,5）：").strip()
            
            target_platforms = []
            for c in choices.split(','):
                idx = int(c.strip()) - 1
                if 0 <= idx < len(platforms):
                    target_platforms.append(platforms[idx])
            
            if not target_platforms:
                target_platforms = ["朋友圈", "小红书"]
            
            print(f"\n🤖 正在改写为 {', '.join(target_platforms)} 版本...")
            result = marketer.repurpose_content(original, target_platforms)
            print("\n" + "=" * 60)
            print(result)
            print("=" * 60)
        
        elif choice == '7':
            history = marketer.list_history()
            if not history:
                print("📭 暂无历史记录")
            else:
                print("\n📚 生成历史：")
                for item in history:
                    print(f"{item['index']}. [{item['platform']}] {item['topic']} - {item['time']}")
                
                idx = input("\n输入序号查看详情（直接回车返回）：").strip()
                if idx.isdigit():
                    idx = int(idx)
                    if 0 <= idx < len(history):
                        print("\n" + marketer.content_history[idx]['content'])
                        save = input("\n是否保存这份内容？(y/n)：").strip().lower()
                        if save == 'y':
                            print(marketer.save_content(idx))
        
        elif choice == '8':
            print("感谢使用，再见！")
            break
        
        else:
            print("❌ 无效选择，请输入1-8")

if __name__ == "__main__":
    main()