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

# ساخت کلاینت تلگرام (مطمئن می‌شویم در یک حلقه درست اجرا شود)
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

def start_bot():
    # ساختن یک حلقه asyncio جدید برای ترد ربات
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

if __name__ == '__main__':
    # اجرای ربات در یک ترد جداگانه با حلقه مخصوص به خود
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    # اجرای سرور وب در ترد اصلی (برای جلوگیری از خطای پورت تکراری)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
