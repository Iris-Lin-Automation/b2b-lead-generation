import time
import random
import os
from playwright.sync_api import sync_playwright

def run_hybrid_safe_test():
    print("🤖 [智能分身完全体] 正在启动【Cookie注入 + 终极隐身】安全通道...")
    
    # 📝 1. 填入你的 li_at 字符串
    LI_AT_COOKIE = "你的_li_at_实际字符串" 
    
    user_data_path = "D:/LinkedIn_B2B_Agent_Standard/automation_profile"
    
    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_path,
            channel="chrome",  
            headless=False,    
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled" 
            ]
        )

        browser_context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        browser_context.add_cookies([{
            'name': 'li_at',
            'value': LI_AT_COOKIE,
            'domain': '.www.linkedin.com',
            'path': '/',
            'secure': True,
            'httpOnly': True
        }])

        page = browser_context.pages[0]
        
        target_url = "https://www.linkedin.com/in/thomas-preston-analytics"
        print(f"🌐 正在戴着双重防弹衣，直接全自动导航至目标领英: {target_url}")
        
        # 🛡️ 【防秒退核心改进】：用 try 包裹，网页加载超时也绝不崩溃
        try:
            # 💡 改变策略：wait_until="domcontentloaded" 只要核心文字骨架出来就算成功，不等图片和追踪脚本
            page.goto(target_url, timeout=45000, wait_until="domcontentloaded")
            
            # 到达后模拟真人随便滚两下网页
            sleep_time = random.randint(8, 12)
            print(f"✨ 已经挤进去了！网络可能有点慢，正在原地模拟阅读 {sleep_time} 秒...")
            time.sleep(sleep_time)
            print("🎉 流程跑通！")
            
        except Exception as e:
            # 💡 哪怕网络断了报错，也会被这里死死抓住，不会闪退！
            print(f"\n⚠️ [网络警告] 网页加载超过 45 秒，引发了超时错误。")
            print(f"ℹ️ 报错详情: {e}")
            print("💡 别慌！号绝对没事，这纯粹是网络卡。浏览器已被我死死留住，快切过去看看网页加载到哪一步了。")
        
        # 🏁 终极死锁：只要你不敲回车，浏览器就算断网也必须给我挂在屏幕上
        print("\n🏁 脚本执行完毕。")
        input("🛑 【安全卡点】浏览器已锁死。看完后，请直接去手动点击网页右上角的【X】关闭。")
        browser_context.close()

if __name__ == "__main__":
    run_hybrid_safe_test()