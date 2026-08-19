import asyncio
import os
import requests  # این کتابخانه جدید برای بیدار نگه داشتن است
from telethon import TelegramClient
from flask import Flask
import threading

# دریافت متغیرهای محیطی
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '')
CHAT_ID = int(os.environ.get('CHAT_ID', 0))
INTERVAL_SECONDS = 280

print("✅ متغیرهای محیطی خوانده شدند.")

# تنظیم سرور وب
app = Flask(__name__)
@app.route('/')
def home():
    return "ربات در حال کار است!"

async def bot_loop():
    while True:
        try:
            client = TelegramClient('session_mew', API_ID, API_HASH)
            await client.connect()
            
            if not await client.is_user_authorized():
                print("📱 در حال تلاش برای اتصال...")
                await client.disconnect()
                await asyncio.sleep(60)
                continue

            print("✅ ربات به تلگرام متصل شد!")
            while True:
                await client.send_message(CHAT_ID, "میو")
                print("📨 'میو' ارسال شد.")
                await asyncio.sleep(INTERVAL_SECONDS)
                
        except Exception as e:
            print(f"❌ خطا (تلاش مجدد در ۶۰ ثانیه): {e}")
            await asyncio.sleep(60)

# --- تابع جدید برای بیدار نگه داشتن سرویس ---
def keep_alive():
    url = os.environ.get('RENDER_EXTERNAL_URL', '') # آدرس سایت را خودکار پیدا می‌کند
    if not url:
        url = "https://my-mewo-bot.onrender.com" # اگر پیدا نکرد، این یکی را بزن
    while True:
        try:
            requests.get(url)
            print("💡 درخواست بیدارباش به سرور ارسال شد.")
        except:
            pass
        time.sleep(30) # هر ۳۰ ثانیه یکبار به خودش درخواست می‌فرستد
# -------------------------------------------------

threading.Thread(target=lambda: asyncio.run(bot_loop()), daemon=True).start()

# اجرای تابع بیدارباش در یک ترد جداگانه
import time
threading.Thread(target=keep_alive, daemon=True).start()

port = int(os.environ.get('PORT', 10000))
app.run(host='0.0.0.0', port=port, debug=False)
