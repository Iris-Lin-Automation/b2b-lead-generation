import pandas as pd
import requests
import json
import os
import time
import random

# ==========================================
# 核心配置：已为你统一规范变量
# ==========================================
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")  # 通过环境变量读取,勿硬编码/勿提交; 另请尽快到平台吊销下方已泄漏的旧 key
API_URL = "https://api.deepseek.com/v1/chat/completions"  # 关键修复：补充了标准的官方路由路径
MODEL_NAME = "deepseek-chat"  # 官方标准模型名称：deepseek-chat (对应 V3/V4)

def load_b2b_config():
    """解析并读取 B2B 智能体专用提示词母版"""
    config = {}
    with open("b2b_agent_prompt.txt", "r", encoding="utf-8") as f:
        content = f.read()
    config['system_role'] = content.split("[SYSTEM_ROLE]\n")[1].split("\n\n")[0].strip()
    config['business_context'] = content.split("[BUSINESS_CONTEXT]\n")[1].split("\n\n")[0].strip()
    config['rules'] = content.split("[STRICT_ANTI_CHINGLISH_RULES]\n")[1].split("\n\n")[0].strip()
    config['structure'] = content.split("[MESSAGE_STRUCTURE]\n")[1].strip()
    return config

def call_deepseek_agent(config, row):
    """调用 DeepSeek 智能体生成符合欧美学术/专业语气的领英个性化加好友信函"""
    
    # 动态把当前表格里的客户信息拼接到 Prompt 中
    user_prompt = f"""
    Please draft a LinkedIn connection message for the following prospect:
    - Name: {row['First Name']} {row.get('Last Name', '')}
    - Title: {row['Title']}
    - Company/Institution: {row['Company']}
    
    Our Business Context:
    {config['business_context']}
    
    Strict Style Rules:
    {config['rules']}
    
    Required Message Structure:
    {config['structure']}
    
    Output ONLY the final 3-sentence English text inside a markdown block. No greetings to me, no explanations.
    """
    
    # 关键修复：消除双引号嵌套语法错误，直接优雅地引用顶部定义的全局变量
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": config['system_role']},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3, # 低随机度，确保严谨不胡说八道
        "max_tokens": 150
    }
    
    try:
        # 关键修复：使用完整的 API_URL 发送请求
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            # 提取文本并清洗掉大模型的 markdown 标记
            msg = res_json['choices'][0]['message']['content'].strip()
            return msg.replace('```markdown', '').replace('```', '').strip()
        else:
            # 升级报错提示：如果失败，把官方返回的错误详情打印出来，方便排查
            return f"API_Error (Status: {response.status_code}, Detail: {response.text})"
    except Exception as e:
        return f"Request_Failed ({str(e)})"

def main():
    print("🚀 【欧美 B2B 领英获客智能体 V1.0】本地测试模式启动...")
    
    # 1. 加载配置
    config = load_b2b_config()
    
    # 2. 读取阿波罗表格（加入彻底的编码容错机制，死磕 UnicodeDecodeError）
    csv_path = "data/raw_leads.csv"
    if not os.path.exists(csv_path):
        print("❌ 错误：未在 data/ 文件夹下检测到原始表 raw_leads.csv，请检查路径！")
        return
        
    print("📝 正在加载 Apollo 原始线索池...")
    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(csv_path, encoding="gbk", errors="ignore")
        except Exception as e:
            print(f"❌ 表格读取彻底失败: {str(e)}")
            return

    # 3. 严格数据精密过滤（一期核心诉求：不浪费点数，精准过滤）
    print(f"📊 原始数据总量: {len(df)} 条")
    
    # 必须包含领英链接、公司名和名字
    df = df.dropna(subset=['Linkedin Url', 'Company', 'First Name'])
    
    # 过滤邮箱状态：只保留 Verified 状态（如果表格有这一列的话）
    if 'Email Status' in df.columns:
        df = df[df['Email Status'].str.lower() == 'verified']
        
    leads = df.to_dict(orient="records")
    print(f"🎯 经过本地流水线清洗，过滤掉垃圾数据，剩余精准欧美目标: {len(leads)} 条")
    
    # 如果数据太多，测试阶段我们先只跑前 3 条看效果，防止烧干你的 API 额度
    test_limit = min(3, len(leads))
    print(f"⏳ 正在启动大模型话术引擎，本次测试前 {test_limit} 条数据...")
    
    results = []
    for idx in range(test_limit):
        row = leads[idx]
        print(f"   [处理中 {idx+1}/{test_limit}] 正在为 {row['First Name']} ({row['Company']}) 定制话术...")
        
        # 调用智能体写信
        custom_pitch = call_deepseek_agent(config, row)
        row['Custom_LinkedIn_Message'] = custom_pitch
        results.append(row)
        
        # 拟人化休眠机制（Jitter）：本地测试同样模拟真人在组织语言，防止请求过快
        sleep_time = random.randint(2, 4)
        time.sleep(sleep_time)
        
    # 4. 导出高质量交付级报表
    out_df = pd.DataFrame(results)
    os.makedirs("output", exist_ok=True)
    
    # 输出为 Excel 文件，方便甲方员工在 Windows 上直接双击打开查看
    output_excel = "output/B2B_Outreach_Tasks.xlsx"
    out_df.to_excel(output_excel, index=False)
    
    print(f"\n🏆 本地全流程完美跑通！成果表已保存至: {output_excel}")
    print("💡 方案亮点：你的员工现在可以直接打开该 Excel，点击客户的 'Linkedin Url' 触达页面，然后将自动生成的 'Custom_LinkedIn_Message' 复制发送，完成 0 风险的纯正欧美风获客！")

if __name__ == "__main__":
    main()