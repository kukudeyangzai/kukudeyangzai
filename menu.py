# 保险代理人智能工具集 - 一键启动菜单
import os
import subprocess

tools = {
    "1": {"name": "💬 基础问答", "file": "simple_chat.py"},
    "2": {"name": "🎭 三种话术风格", "file": "sticky_chat.py"},
    "3": {"name": "💭 多轮对话", "file": "memory_chat.py"},
    "4": {"name": "📚 知识库问答", "file": "kb_chat.py"},
    "5": {"name": "📊 产品对比", "file": "product_compare.py"},
    "6": {"name": "📝 计划书生成", "file": "proposal_generator.py"},
    "7": {"name": "👥 客户管理", "file": "customer_manager.py"},
    "8": {"name": "📱 内容营销", "file": "content_marketing.py"},
    "9": {"name": "🏥 理赔助手", "file": "claim_assistant.py"},
    "10": {"name": "🎂 生日提醒", "file": "birthday_reminder.py"},
    "11": {"name": "🔍 保单体检", "file": "policy_check.py"},
    "12": {"name": "🎯 AI陪练", "file": "ai_training.py"},
}

while True:
    print("\n" + "="*60)
    print("          保险代理人智能工具集 v2.0")
    print("="*60)
    for key, tool in tools.items():
        print(f"{key}. {tool['name']}")
    print("0. 退出")
    print("-"*60)
    
    choice = input("\n请选择工具（输入数字）：").strip()
    
    if choice == "0":
        print("感谢使用，再见！")
        break
    elif choice in tools:
        file = tools[choice]['file']
        if os.path.exists(file):
            print(f"\n🚀 启动 {tools[choice]['name']}...")
            print("="*60)
            subprocess.run(["python", file])
            input("\n按回车键返回主菜单...")
        else:
            print(f"❌ 文件 {file} 不存在，请先创建")
    else:
        print("❌ 无效选择，请输入0-12")