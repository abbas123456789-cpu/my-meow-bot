import asyncio
import os
from telethon import TelegramClient
from flask import Flask
import threading

API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '')
CHAT_ID = int(os.environ.get('CHAT_ID', 0))
INTERVAL_SECONDS = 283

print("✅ متغیرهای محیطی خوانده شدند.")
print("⏳ در حال راه‌اندازی سرور و ربات...")

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
                print("📱 تلگرام از ما کد تایید خواست! در حال ارسال درخواست...")
                await client.send_code_request(PHONE_NUMBER)
                print("⏳ کد به گوشی شما ارسال شد. اما چون شما در Render هستید، منتظر کد نمی‌مانیم!")
                print("🔄 ۶۰ ثانیه صبر می‌کنیم و دوباره تلاش می‌کنیم تا خودش لاگین شود...")
                await client.disconnect()
                await asyncio.sleep(60)
                continue

            print("✅ ربات با موفقیت به تلگرام متصل شد! (فایل نشست ساخته شد)")
            
            # حلقه ارسال پیام
            while True:
                try:
                    await client.send_message(CHAT_ID, "میو")
                    print("📨 پیام 'میو' ارسال شد.")
                except Exception as e:
                    print(f"❌ خطا در ارسال: {e}")
                await asyncio.sleep(INTERVAL_SECONDS)
                
        except Exception as e:
            print(f"❌ خطای کلی (تلاش مجدد در ۶۰ ثانیه): {e}")
            await asyncio.sleep(60)

def run_async():
    asyncio.run(bot_loop())

if __name__ == '__main__':
    print("🚀 ربات در حال اجرا است...")
    threading.Thread(target=run_async, daemon=True).start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
