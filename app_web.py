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
if 'agent_name' not in st.session_state:
    st.session_state['agent_name'] = '张经理'
if 'agent_company' not in st.session_state:
    st.session_state['agent_company'] = '中汇保险'

# 侧边栏导航
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/insurance-agent.png", width=80)
    st.title("🛡️ 保险智能助手")
    st.markdown("---")
    
    # 用户信息
    st.subheader("👤 代理人信息")
    agent_name = st.text_input("姓名", value=st.session_state.agent_name, key="agent_name_input")
    agent_company = st.text_input("公司", value=st.session_state.agent_company, key="agent_company_input")
    
    # 更新session_state
    st.session_state.agent_name = agent_name
    st.session_state.agent_company = agent_company
    
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
         "📈 数据分析"],
        key="navigation"
    )
    
    st.markdown("---")
    st.caption(f"© 2026 {st.session_state.agent_name} | 中汇保险 v2.0")

# ==================== 首页看板 ====================
if page == "🏠 首页看板":
    st.title("🏠 智能保险助手首页")
    
    # 欢迎语
    st.markdown(f"""
    ### 早上好，{st.session_state.agent_name}！ 👋
    今天是 {datetime.now().strftime('%Y年%m月%d日 %A')}
    """)
    
    # 核心指标
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
        if st.button("💬 快速问答", key="btn1", use_container_width=True):
            st.session_state['page'] = "💬 AI智能问答"
            st.rerun()
    with col2:
        if st.button("📊 产品对比", key="btn2", use_container_width=True):
            st.session_state['page'] = "📊 产品对比"
            st.rerun()
    with col3:
        if st.button("📝 生成计划书", key="btn3", use_container_width=True):
            st.session_state['page'] = "📝 计划书生成"
            st.rerun()
    with col4:
        if st.button("🏥 理赔分析", key="btn4", use_container_width=True):
            st.session_state['page'] = "🏥 理赔助手"
            st.rerun()
    
    # 待办事项和业绩
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
    
    # 初始化对话历史
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # 显示历史消息
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 用户输入
    if prompt := st.chat_input("请输入你的问题..."):
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI回复
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                # 简单回复示例
                response = f"关于「{prompt}」的问题，根据中汇保险的产品条款..."
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# ==================== 产品对比 ====================
elif page == "📊 产品对比":
    st.title("📊 保险产品对比")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 产品A")
        product1_name = st.text_input("产品名称", value="中汇福2025", key="p1_name")
        product1_type = st.selectbox("产品类型", ["重疾险", "医疗险", "意外险", "寿险", "年金险"], key="p1_type")
        product1_desc = st.text_area("产品描述", value="重疾险，保终身，50万保额，30年缴", key="p1_desc", height=100)
    
    with col2:
        st.subheader("📦 产品B")
        product2_name = st.text_input("产品名称", value="中汇安康2025", key="p2_name")
        product2_type = st.selectbox("产品类型", ["重疾险", "医疗险", "意外险", "寿险", "年金险"], key="p2_type")
        product2_desc = st.text_area("产品描述", value="重疾险，保终身，50万保额，20年缴", key="p2_desc", height=100)
    
    if st.button("开始对比", type="primary", use_container_width=True):
        st.markdown("### 📊 对比结果")
        
        # 对比表格
        compare_df = pd.DataFrame({
            '对比维度': ['产品类型', '保障期限', '保额', '缴费期', '等待期', '轻症保障', '身故保障'],
            product1_name: [product1_type, '终身', '50万', '30年', '90天', '3次赔付', '赔付保额'],
            product2_name: [product2_type, '终身', '50万', '20年', '180天', '2次赔付', '赔付保额']
        })
        st.dataframe(compare_df, use_container_width=True, hide_index=True)
        
        # 建议
        st.info("💡 建议：如果看重轻症保障可选产品A，如果希望快速缴清可选产品B")

# ==================== 计划书生成 ====================
elif page == "📝 计划书生成":
    st.title("📝 保险计划书生成")
    
    with st.expander("客户信息", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("姓名", "张先生")
            age = st.number_input("年龄", 0, 100, 35)
            gender = st.selectbox("性别", ["男", "女"])
        with col2:
            occupation = st.text_input("职业", "企业职员")
            income = st.selectbox("年收入", ["10万以下", "10-20万", "20-50万", "50万以上"])
            marriage = st.selectbox("婚姻状况", ["已婚", "未婚", "离异"])
        with col3:
            children = st.number_input("子女数量", 0, 10, 1)
            budget = st.number_input("预算(元/年)", 0, 100000, 8000, step=1000)
            needs = st.multiselect("保障需求", ["重疾", "医疗", "意外", "寿险", "养老"], ["重疾", "医疗"])
    
    if st.button("生成计划书", type="primary", use_container_width=True):
        st.markdown(f"""
        ### 📄 保险计划书（草稿）
        
        **尊敬的{name}：**
        
        根据您的需求和预算，我们为您推荐以下中汇保险保障方案：
        
        | 产品类型 | 推荐产品 | 保额 | 保费/年 |
        |---------|---------|------|--------|
        | 重疾险 | 中汇福2025 | 50万 | 5,500元 |
        | 医疗险 | 中汇安享医疗 | 200万 | 800元 |
        | 意外险 | 中汇安心保 | 100万 | 500元 |
        
        **总保费：6,800元/年**
        
        如需进一步调整方案，请随时联系。
        """)
        
        st.download_button("下载计划书", f"{name}的保险计划书", f"{name}_计划书.txt")

# ==================== 客户管理 ====================
elif page == "👥 客户管理":
    st.title("👥 客户管理")
    
    tab1, tab2, tab3 = st.tabs(["📋 客户列表", "➕ 添加客户", "📊 客户分析"])
    
    with tab1:
        # 客户数据
        customers = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5],
            '姓名': ['王小明', '李芳', '张伟', '刘洋', '陈静'],
            '电话': ['138****0001', '138****0002', '138****0003', '138****0004', '138****0005'],
            '年龄': [35, 42, 28, 55, 31],
            '状态': ['意向强', '跟进中', '已签单', '犹豫', '待联系'],
            '产品意向': ['重疾险', '医疗险', '意外险', '重疾险', '养老险'],
            '最后联系': ['2026-03-08', '2026-03-07', '2026-03-05', '2026-03-01', '2026-02-28']
        })
        st.dataframe(customers, use_container_width=True, hide_index=True)
        
        # 客户详情
        selected = st.selectbox("选择客户查看详情", customers['姓名'].tolist())
        if selected:
            with st.expander("客户详情"):
                st.json({
                    "姓名": selected,
                    "沟通记录": [
                        "2026-03-08：电话沟通重疾险，对价格敏感",
                        "2026-03-01：发送中汇保险产品资料",
                        "2026-02-25：首次接触，了解需求"
                    ]
                })
    
    with tab2:
        st.info("添加新客户")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("姓名*", key="new_name")
            st.text_input("电话*", key="new_phone")
            st.number_input("年龄", 0, 100, 30, key="new_age")
        with col2:
            st.selectbox("性别", ["男", "女"], key="new_gender")
            st.text_input("职业", key="new_job")
            st.text_input("来源", "朋友介绍", key="new_source")
        st.text_area("备注", key="new_note")
        if st.button("保存客户"):
            st.success("客户添加成功！")
    
    with tab3:
        st.subheader("AI客户分析")
        customer_for_analysis = st.selectbox("选择客户", ["王小明", "李芳", "张伟"])
        if st.button("开始分析"):
            with st.spinner("AI正在分析..."):
                st.progress(100)
                st.metric("购买意愿", "85%", "+12%")
                st.info("推荐产品：中汇福重疾险+中汇安享医疗险组合")
                st.info("下一步建议：本周发送计划书，周五跟进")

# ==================== 内容营销 ====================
elif page == "📱 内容营销":
    st.title("📱 内容营销")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        platform = st.selectbox("选择平台", ["朋友圈", "公众号", "小红书", "抖音脚本", "知乎回答"])
        style = st.selectbox("风格", ["通俗易懂", "专业严谨", "温暖共情"])
        topic = st.text_input("主题", "重疾险为什么重要")
        keywords = st.text_input("关键词", "重疾险,保障,家庭,中汇保险")
        
        if st.button("生成文案", type="primary", use_container_width=True):
            st.session_state['generated_content'] = f"""
### 标题：为什么每个家庭都需要重疾险？

{platform}平台专属文案（{style}风格）：

重疾险不是花钱，是给未来的自己留一条后路。

当中汇保险客户遇到疾病时，重疾险能给你：
1️⃣ 一笔现金，自由支配
2️⃣ 治疗期间的家庭开支保障
3️⃣ 安心养病，不用担心收入中断

#重疾险 #家庭保障 #中汇保险 #保险科普
            """
    
    with col2:
        st.subheader("📝 生成内容")
        if 'generated_content' in st.session_state:
            st.markdown(st.session_state.generated_content)
            st.download_button("下载文案", st.session_state.generated_content, "营销文案.txt")
        else:
            st.info("点击左侧「生成文案」按钮开始创作")

# ==================== 理赔助手 ====================
elif page == "🏥 理赔助手":
    st.title("🏥 中汇保险理赔智能助手")
    
    tab1, tab2, tab3 = st.tabs(["🔍 理赔分析", "📋 材料清单", "📊 数据看板"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            diagnosis = st.text_input("诊断结果", "甲状腺癌")
            policy_type = st.selectbox("保险类型", ["重疾险", "医疗险", "意外险", "寿险"])
        with col2:
            amount = st.number_input("申请金额", 0, 1000000, 500000, step=10000)
            hospital = st.text_input("就诊医院", "市人民医院")
        
        if st.button("开始分析", key="analyze_btn"):
            st.markdown("""
            ### 🔍 理赔分析结果
            
            **中汇保险理赔评估：**
            - ✅ 符合理赔条件：是
            - 💰 预估赔付金额：50万元
            - ⏱️ 预估处理时间：5-7个工作日
            - ⚠️ 注意事项：需提供完整病理报告
            
            **理赔流程：**
            1. 准备材料（3-5天）
            2. 提交申请（1天）
            3. 保险公司审核（5天）
            4. 赔款到账（1-2天）
            """)
    
    with tab2:
        st.subheader("📋 理赔所需材料清单")
        
        claim_type = st.radio("选择理赔类型", ["重疾险", "医疗险", "意外险", "身故险"], horizontal=True)
        
        if claim_type == "重疾险":
            st.checkbox("✅ 理赔申请书")
            st.checkbox("✅ 被保险人身份证")
            st.checkbox("✅ 银行卡复印件")
            st.checkbox("✅ 诊断证明书（原件）")
            st.checkbox("✅ 病理检验报告")
            st.checkbox("✅ 出院小结")
            st.checkbox("✅ 保单原件")
            
            st.progress(60, text="材料准备进度")
            st.info("缺病理报告原件，请联系医院补办")
    
    with tab3:
        st.subheader("📊 中汇保险理赔数据")
        
        # 模拟数据
        df = pd.DataFrame({
            '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
            '理赔金额(万)': [45, 78, 62, 89, 120, 95],
            '案件数量': [8, 12, 10, 15, 18, 14]
        })
        
        col1, col2, col3 = st.columns(3)
        col1.metric("总理赔金额", "489万", "+15%")
        col2.metric("总案件数", "77件", "8")
        col3.metric("平均赔付", "6.4万", "+5%")
        
        fig = px.bar(df, x='月份', y='理赔金额(万)', title='中汇保险月度理赔金额趋势')
        st.plotly_chart(fig, use_container_width=True)
        
        # 导出功能
        csv = df.to_csv(index=False)
        st.download_button("📥 导出理赔数据", csv, "中汇保险_理赔数据.csv")

# ==================== 保单体检 ====================
elif page == "🔍 保单体检":
    st.title("🔍 保单体检")
    
    st.info("上传客户现有保单，AI分析保障缺口")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 现有保单")
        policies = st.text_area("输入保单信息", 
                               value="中汇福重疾险 50万\n中汇安享医疗险 200万\n中汇安心意外险 100万",
                               height=150)
    
    with col2:
        st.subheader("👤 客户信息")
        age = st.number_input("年龄", 30)
        income = st.number_input("年收入(万)", 20)
        debt = st.number_input("负债(万)", 50)
        dependents = st.number_input("抚养人数", 2)
    
    if st.button("开始体检", type="primary"):
        st.markdown("""
        ### 📊 保单体检报告
        
        **保障完整性分析：**
        - ✅ 重疾保障：50万（合理）
        - ✅ 医疗保障：200万（充足）
        - ✅ 意外保障：100万（合理）
        - ❌ 寿险保障：缺失（建议补充）
        
        **保障缺口：**
        - 寿险缺口：约100万
        - 建议补充产品：中汇尊享寿险
        
        **优化建议：**
        1. 补充100万定期寿险
        2. 重疾险可考虑加保至80万
        3. 建议增加投保人豁免
        """)

# ==================== 数据分析 ====================
elif page == "📈 数据分析":
    st.title("📈 中汇保险业务数据分析")
    
    # 业绩趋势
    st.subheader("📊 业绩趋势")
    
    data = pd.DataFrame({
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '保费收入(万)': [12, 18, 15, 22, 28, 25],
        '签单数': [4, 6, 5, 8, 10, 9]
    })
    
    fig = px.line(data, x='月份', y=['保费收入(万)', '签单数'], title='月度业绩趋势')
    st.plotly_chart(fig, use_container_width=True)
    
    # 产品销售分布
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🍩 产品销售分布")
        product_data = pd.DataFrame({
            '产品类型': ['重疾险', '医疗险', '意外险', '寿险', '年金险'],
            '销售占比': [45, 25, 15, 10, 5]
        })
        fig2 = px.pie(product_data, values='销售占比', names='产品类型', title='中汇保险产品销售占比')
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.subheader("📊 客户来源分析")
        source_data = pd.DataFrame({
            '来源': ['朋友介绍', '老客户', '线上', '线下活动', '其他'],
            '数量': [28, 15, 12, 8, 5]
        })
        fig3 = px.bar(source_data, x='来源', y='数量', title='客户来源分布')
        st.plotly_chart(fig3, use_container_width=True)
    
    # 数据导出
    st.subheader("📥 数据导出")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("导出业绩报表"):
            csv = data.to_csv(index=False)
            st.download_button("下载CSV", csv, "中汇保险_业绩报表.csv")
    with col2:
        if st.button("导出客户分析"):
            st.info("报表生成中...")

# 底部
st.markdown("---")
st.caption(f"中汇保险智能助手 | 代理人：{st.session_state.agent_name} | 基于火山引擎豆包大模型")