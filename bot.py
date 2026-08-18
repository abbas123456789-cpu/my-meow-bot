import asyncio
import os
from telethon import TelegramClient
from flask import Flask
import threading

# دریافت متغیرهای محیطی
api_id = int(os.environ.get('API_ID', 0))
api_hash = os.environ.get('API_HASH', '')
phone = os.environ.get('PHONE_NUMBER', '')
chat_id = int(os.environ.get('CHAT_ID', 0))

INTERVAL_SECONDS = 286

# بررسی وجود متغیرها
if not api_id or not api_hash or not phone or not chat_id:
    print("خطا: متغیرهای محیطی تنظیم نشده‌اند.")
    exit(1)

# ساخت کلاینت تلگرام
client = TelegramClient('session_mew', api_id, api_hash)

async def send_mew():
    try:
        await client.start(phone)
        print("ربات متصل شد و در حال ارسال پیام است...")
        await client.send_message(chat_id, "میو")
        print("پیام 'میو' ارسال شد.")
    except Exception as e:
        print(f"خطا در ارسال پیام: {e}")

async def main():
    print("ربات شروع به کار کرد.")
    while True:
        await send_mew()
        await asyncio.sleep(INTERVAL_SECONDS)

# تنظیم سرور وب (فقط برای راضی کردن Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات تلگرام در حال کار است!"

if __name__ == '__main__':
    # راه‌اندازی سرور وب
    port = int(os.environ.get('PORT', 10000))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False), daemon=True).start()
    
    # اجرای ربات اصلی
    asyncio.run(main())
