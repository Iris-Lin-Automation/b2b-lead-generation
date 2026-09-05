import pandas as pd
import os

def clean_apollo_leads(input_file, output_file, target_keywords):
    print("      开始执行 Apollo 原始数据精密清洗...")
    
    # 彻底解决你之前遇到的 UnicodeDecodeError 编码崩溃问题
    try:
        df = pd.read_csv(input_file, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(input_file, encoding="gbk", errors="ignore")
        
    print(f"原始数据共加载: {len(df)} 条线索。")
    
    # 规则 1：必须有领英链接，必须有公司名称
    df = df.dropna(subset=['Linkedin Url', 'Company', 'Title'])
    
    # 规则 2：企业邮箱状态必须是 Verified（确保触达率，不浪费额度）
    # 注意：Apollo导出的字段名通常是 'Email Status'
    if 'Email Status' in df.columns:
        df = df[df['Email Status'].str.lower() == 'verified']
        
    # 规则 3：关键词二次精密匹配（Title 或 Bio 包含特定关键词才要）
    # 把关键词变成小写，防止大小写不一致漏掉数据
    keywords_lower = [kw.lower() for kw in target_keywords]
    
    def match_keywords(row):
        title_text = str(row['Title']).lower()
        # 有些表格有 'Biography' 或 'Keywords'，这里以 Title 为核心
        return any(kw in title_text for kw in keywords_lower)
    
    df = df[df.apply(match_keywords, axis=1)]
    
    # 只抽取我们后面流程需要用的核心字段，减少传输体积
    core_columns = ['First Name', 'Last Name', 'Title', 'Company', 'Email', 'Linkedin Url']
    df_cleaned = df[core_columns]
    
    # 自动创建输出文件夹并保存
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df_cleaned.to_csv(output_file, index=False, encoding="utf-8")
    
    print(f" 清洗完毕！已剔除垃圾数据。剩余精准目标: {len(df_cleaned)} 条。文件已保存至: {output_file}")

if __name__ == "__main__":
    # 模拟甲方的业务场景
    INPUT_PATH = "data/raw_leads.csv"  # 放阿波罗导出的原始表
    OUTPUT_PATH = "data/cleaned_leads.csv" # 产出的精准池
    
    # 甲方要的特定垂直行业关键词
    KEYWORDS = ["SRE", "Site Reliability", "Infrastructure", "Platform Engineer"]
    
    clean_apollo_leads(INPUT_PATH, OUTPUT_PATH, KEYWORDS)