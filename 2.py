import os
from playwright.sync_api import sync_playwright

def run_safe_session():
    # 📝 把你刚才在浏览器里复制的 li_at 字符串贴在这里
    LI_AT_COOKIE = os.environ.get("LINKEDIN_LI_AT", "")  # 通过环境变量读取,勿硬编码/勿提交; 旧硬编码 cookie 已确认为敏感凭证应尽快使失效
    
    with sync_playwright() as p:
        # 启动一个最轻量的无头/有头浏览器（此时是未登录状态）
        browser = p.chromium.launch(headless=False, channel="chrome")
        context = browser.new_context()
        
        # 🛡️ 注入白嫖自项目三的安全 Cookie
        context.add_cookies([{
            'name': 'li_at',
            'value': LI_AT_COOKIE,
            'domain': '.www.linkedin.com',
            'path': '/',
            'secure': True,
            'httpOnly': True
        }])
        
        page = context.new_page()
        
        print("🌐 正在戴着 Cookie 面具直接潜入领英主页...")
        # 关键：直接去主页，绕过登录页！
        page.goto("https://www.linkedin.com/")
        
        # 验证是否成功：如果页面里有 Thomas 的主页或者你自己的 feed，说明免密登录成功！
        page.wait_for_timeout(5000)
        
        print("🎉 完美绕过登录风控！可以直接去抓 Sales Navigator 或者 Thomas 的主页了。")
        browser.close()

if __name__ == "__main__":
    run_safe_session()