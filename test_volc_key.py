import os
from dotenv import load_dotenv

# 加载环境变量（从 .env 文件中读取密钥和ID）
load_dotenv()

# 从环境变量中读取API密钥和接入点ID
# 【修改点1】变量名从 VOLC_API_KEY 改为 ARK_API_KEY
ARK_API_KEY = os.getenv("ARK_API_KEY")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

# 打印读取到的密钥和ID（生产环境建议隐藏部分字符）
print("读取到的API密钥：", ARK_API_KEY[:6] + "..." if ARK_API_KEY else "未找到")
print("读取到的接入点ID：", ENDPOINT_ID)

# 检查密钥和ID是否为空
if not ARK_API_KEY:
    print("❌ 错误：未读取到API密钥，请检查.env文件配置")
elif not ENDPOINT_ID:
    print("❌ 错误：未读取到接入点ID，请检查.env文件配置")
else:
    print("✅ 成功读取到API密钥和接入点ID！")
    
    # 检查密钥和ID格式是否正确
    # 【修改点2】检查前缀是否为 "ak"
    if ARK_API_KEY.startswith("ak") and len(ARK_API_KEY) >= 20:
        print("✅ API密钥格式正确")
    else:
        print("❌ 错误：API密钥格式不正确，请检查是否复制正确（应以'ak'开头）")
        
    if ENDPOINT_ID.startswith("ep-") and len(ENDPOINT_ID) >= 20:
        print("✅ 接入点ID格式正确")
    else:
        print("❌ 错误：接入点ID格式不正确，请检查是否复制正确（应以'ep-'开头）")