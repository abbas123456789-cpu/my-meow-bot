import asyncio
import os
from telethon import TelegramClient
from flask import Flask
import threading

# دریافت متغیرهای محیطی از تنظیمات Render
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '')
CHAT_ID = int(os.environ.get('CHAT_ID', 0))
INTERVAL_SECONDS = 286

# بررسی اینکه متغیرها پر شده‌اند یا خیر
if not API_ID or not API_HASH or not PHONE_NUMBER or not CHAT_ID:
    print("خطا: متغیرهای محیطی تنظیم نشده‌اند.")
    exit(1)

# تنظیم سرور وب برای اینکه Render خاموش نشود
app = Flask(__name__)
@app.route('/')
def home():
    return "ربات در حال کار است!"

# ساخت کلاینت (به فایل session_mew.session نیاز دارد)
client = TelegramClient('session_mew', API_ID, API_HASH)

async def send_mew():
    try:
        await client.send_message(CHAT_ID, "میو")
        print("پیام 'میو' ارسال شد.")
    except Exception as e:
        print(f"خطا در ارسال پیام: {e}")

async def bot_loop():
    try:
        # سعی می‌کنیم لاگین کنیم
        await client.start(PHONE_NUMBER)
        print("ربات با موفقیت به تلگرام متصل شد و پیام‌ها را ارسال می‌کند!")
        while True:
            await send_mew()
            await asyncio.sleep(INTERVAL_SECONDS)
    except Exception as e:
        print(f"خطای بحرانی ربات: {e}")
        await asyncio.sleep(60)

def run_async():
    asyncio.run(bot_loop())

if __name__ == '__main__':
    # اجرای ربات در یک ترد جداگانه
    bot_thread = threading.Thread(target=run_async, daemon=True)
    bot_thread.start()
    # اجرای سرور وب
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
