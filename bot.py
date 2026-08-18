import asyncio
import os
from telethon import TelegramClient
from flask import Flask  # اضافه کردن کتابخانه برای سرور
import threading

# متغیرهای محیطی
api_id = int(os.environ.get('API_ID', 0))
api_hash = os.environ.get('API_HASH', '')
phone = os.environ.get('PHONE_NUMBER', '')
chat_id = int(os.environ.get('CHAT_ID', 0))

INTERVAL_SECONDS = 286

# بررسی وجود متغیرها
if not api_id or not api_hash or not phone or not chat_id:
    print("خطا: متغیرهای محیطی تنظیم نشده‌اند.")
    exit(1)

async def send_mew():
    client = TelegramClient('session_mew', api_id, api_hash)
    try:
        await client.start(phone)
        print("ربات وارد شد.")
        await client.send_message(chat_id, "میو")
        print("پیام 'میو' ارسال شد.")
    except Exception as e:
        print(f"خطا رخ داد: {e}")
    finally:
        await client.disconnect()

async def main():
    print("ربات شروع به کار کرد.")
    while True:
        await send_mew()
        await asyncio.sleep(INTERVAL_SECONDS)

# --- کد جدید برای رندر (باز کردن پورت) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات در حال اجراست!"

def run_web_server():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # اجرای سرور وب در یک ترد جداگانه تا ربات متوقف نشود
    threading.Thread(target=run_web_server, daemon=True).start()
    # اجرای ربات اصلی
    asyncio.run(main())
