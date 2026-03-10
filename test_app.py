import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# 页面配置
st.set_page_config(
    page_title="保险代理人智能助手", 
    page_icon="🛡️", 
    layout="wide"
)

# 初始化session_state
if 'page' not in st.session_state:
    st.session_state['page'] = '🏠 首页看板'

# 侧边栏导航
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/insurance-agent.png", width=80)
    st.title("🛡️ 保险智能助手")
    st.markdown("---")
    
    # 用户信息
    st.subheader("👤 代理人信息")
    agent_name = st.text_input("姓名", value="张经理", key="agent_name")
    agent_company = st.text_input("公司", value="平安保险", key="agent_company")
    
    st.markdown("---")
    
    # 功能导航
    page = st.radio(
        "选择功能",
        ["🏠 首页看板", 
         "💬 AI智能问答", 
         "📊 产品对比", 
         "📝 计划书生成", 
         "👥 客户管理", 
         "📱 内容营销", 
         "🏥 理赔助手", 
         "🔍 保单体检",
         "📈 数据分析"]
    )
    
    st.markdown("---")
    st.caption(f"© 2026 {agent_name} | v2.0")

# ==================== 首页看板 ====================
if page == "🏠 首页看板":
    st.title("🏠 智能保险助手首页")
    
    # 欢迎语
    st.markdown(f"""
    ### 早上好，{st.session_state.agent_name}！ 👋
    今天是 {datetime.now().strftime('%Y年%m月%d日 %A')}
    """)
    
    # 核心指标 - 修复版
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="今日待跟进客户", value="8", delta="+2")
    with col2:
        st.metric(label="进行中理赔", value="3", delta="-1")
    with col3:
        st.metric(label="本月计划书", value="12", delta="+5")
    with col4:
        st.metric(label="内容曝光", value="1.2w", delta="+18%")
    
    # 快捷入口
    st.subheader("🚀 快捷操作")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("💬 快速问答", key="btn1"):
            st.session_state['page'] = "💬 AI智能问答"
            st.rerun()
    with col2:
        if st.button("📊 产品对比", key="btn2"):
            st.session_state['page'] = "📊 产品对比"
            st.rerun()
    with col3:
        if st.button("📝 生成计划书", key="btn3"):
            st.session_state['page'] = "📝 计划书生成"
            st.rerun()
    with col4:
        if st.button("🏥 理赔分析", key="btn4"):
            st.session_state['page'] = "🏥 理赔助手"
            st.rerun()
    
    # 待办事项
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 今日待办")
        todos = pd.DataFrame({
            '时间': ['09:30', '10:15', '14:00', '15:30'],
            '客户': ['王小明', '李芳', '张伟', '刘洋'],
            '事项': ['方案讲解', '理赔跟进', '签单', '生日问候'],
            '状态': ['待处理', '进行中', '待处理', '待处理']
        })
        st.dataframe(todos, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("📊 本周业绩")
        data = pd.DataFrame({
            '日期': ['周一', '周二', '周三', '周四', '周五'],
            '保费(万)': [1.2, 2.1, 0.8, 2.5, 1.5]
        })
        fig = px.bar(data, x='日期', y='保费(万)', title='本周保费趋势')
        st.plotly_chart(fig, use_container_width=True)

# ==================== AI智能问答 ====================
elif page == "💬 AI智能问答":
    st.title("💬 AI智能问答")
    
    # 简单的问答界面
    with st.chat_message("assistant"):
        st.markdown("你好！我是你的保险智能助手，有什么可以帮你的？")
    
    # 用户输入
    if prompt := st.chat_input("请输入你的问题..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                # 简单回复
                st.markdown(f"关于「{prompt}」的问题，重疾险和医疗险的主要区别是...")

# ==================== 产品对比 ====================
elif page == "📊 产品对比":
    st.title("📊 保险产品对比")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("产品A")
        product1_name = st.text_input("产品名称", key="p1_name", value="平安福2025")
        product1_desc = st.text_area("产品描述", key="p1_desc", height=100, 
                                     value="重疾险，保终身，50万保额")
    
    with col2:
        st.subheader("产品B")
        product2_name = st.text_input("产品名称", key="p2_name", value="国寿福2025")
        product2_desc = st.text_area("产品描述", key="p2_desc", height=100,
                                     value="重疾险，保终身，50万保额")
    
    if st.button("开始对比", type="primary", use_container_width=True):
        st.info("对比分析功能开发中...")
        st.markdown(f"""
        ### 对比结果
        
        | 对比维度 | {product1_name} | {product2_name} |
        |---------|----------------|----------------|
        | 产品类型 | 重疾险 | 重疾险 |
        | 保额 | 50万 | 50万 |
        | 缴费期 | 30年 | 20年 |
        | 等待期 | 90天 | 180天 |
        """)

# ==================== 其他页面 ====================
elif page == "📝 计划书生成":
    st.title("📝 保险计划书生成")
    st.info("计划书生成功能开发中...")
    
    st.text_input("客户姓名", "张先生")
    st.number_input("年龄", 0, 100, 35)
    st.number_input("预算", 0, 100000, 8000)
    if st.button("生成计划书"):
        st.success("计划书生成成功！")

elif page == "👥 客户管理":
    st.title("👥 客户管理")
    st.info("客户管理功能开发中...")
    
    # 简单客户列表
    customers = pd.DataFrame({
        '姓名': ['王小明', '李芳', '张伟'],
        '电话': ['138****0001', '138****0002', '138****0003'],
        '状态': ['意向强', '跟进中', '已签单']
    })
    st.dataframe(customers, use_container_width=True)

elif page == "📱 内容营销":
    st.title("📱 内容营销")
    st.info("内容营销功能开发中...")
    
    platform = st.selectbox("选择平台", ["朋友圈", "公众号", "小红书"])
    topic = st.text_input("主题", "重疾险的重要性")
    if st.button("生成文案"):
        st.markdown("### 生成的文案\n重疾险是家庭保障的基石...")

elif page == "🏥 理赔助手":
    st.title("🏥 理赔智能助手")
    st.info("理赔助手功能开发中...")
    
    diagnosis = st.text_input("诊断结果", "甲状腺癌")
    if st.button("分析理赔"):
        st.markdown("""
        ### 理赔分析结果
        - 符合理赔条件：✅ 是
        - 预估赔付金额：50万
        - 所需材料：诊断证明、病理报告、身份证等
        """)

elif page == "🔍 保单体检":
    st.title("🔍 保单体检")
    st.info("保单体检功能开发中...")

elif page == "📈 数据分析":
    st.title("📈 业务数据分析")
    
    # 简单数据展示
    data = pd.DataFrame({
        '月份': ['1月', '2月', '3月'],
        '保费': [12000, 18000, 15000]
    })
    fig = px.line(data, x='月份', y='保费', title='保费趋势')
    st.plotly_chart(fig, use_container_width=True)

# 底部
st.markdown("---")
st.caption("保险代理人智能助手 | 基于火山引擎豆包大模型")