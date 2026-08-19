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
INTERVAL_SECONDS = 280

print("متغیرهای محیطی با موفقیت خوانده شدند.")

# تنظیم سرور وب
app = Flask(__name__)
@app.route('/')
def home():
    return "ربات تلگرام در حال کار است!"

# ساخت کلاینت
client = TelegramClient('session_mew', API_ID, API_HASH)

async def bot_loop():
    try:
        # تلاش برای اتصال (این بار حتی اگر لاگین نشود، برنامه از کار نمی‌افتد)
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
        print(f"خطای اتصال به تلگرام (مهم نیست، تلاش بعدی): {e}")
        await asyncio.sleep(60)

def run_async():
    asyncio.run(bot_loop())

if __name__ == '__main__':
    print("در حال راه‌اندازی ربات...")
    # اجرای ربات
    bot_thread = threading.Thread(target=run_async, daemon=True)
    bot_thread.start()
    # اجرای سرور وب
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
