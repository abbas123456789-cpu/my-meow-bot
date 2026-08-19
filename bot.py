import asyncio
import os
from telethon import TelegramClient
from flask import Flask
import threading

# دریافت متغیرهای محیطی
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '')
CHAT_ID = int(os.environ.get('CHAT_ID', 0))
INTERVAL_SECONDS = 286

print("متغیرهای محیطی با موفقیت خوانده شدند.")

# تنظیم سرور وب
app = Flask(__name__)
@app.route('/')
def home():
    return "ربات در حال کار است!"

async def bot_loop():
    try:
        # اگر فایل session خراب باشد، خودش آن را حذف می‌کند و یک فایل جدید می‌سازد
        client = TelegramClient('session_mew', API_ID, API_HASH)
        
        await client.start(phone=PHONE_NUMBER)
        print("ربات با موفقیت به تلگرام متصل شد!")
        
        while True:
            try:
                await client.send_message(CHAT_ID, "میو")
                print("پیام 'میو' ارسال شد.")
            except Exception as e:
                print(f"خطا در ارسال پیام: {e}")
            await asyncio.sleep(INTERVAL_SECONDS)
            
    except Exception as e:
        print(f"خطای اتصال (تلاش مجدد): {e}")
        await asyncio.sleep(60)

def run_async():
    asyncio.run(bot_loop())

if __name__ == '__main__':
    print("در حال راه‌اندازی ربات...")
    bot_thread = threading.Thread(target=run_async, daemon=True)
    bot_thread.start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
