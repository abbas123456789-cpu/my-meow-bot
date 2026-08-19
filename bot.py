import asyncio
import os
from telethon import TelegramClient
from flask import Flask
import threading
import sqlite3

# دریافت متغیرهای محیطی
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '')
CHAT_ID = int(os.environ.get('CHAT_ID', 0))
INTERVAL_SECONDS = 280

print("متغیرهای محیطی خوانده شدند.")

# تنظیم سرور وب
app = Flask(__name__)
@app.route('/')
def home():
    return "ربات در حال کار است!"

async def bot_loop():
    while True:
        try:
            # مهم: اگر فایل خالی یا خراب باشد، این دستور آن را حذف می‌کند
            session_file = 'session_mew.session'
            if os.path.exists(session_file) and os.path.getsize(session_file) == 0:
                print("⚠️ فایل نشست خالی پیدا شد! در حال حذف و ساخت مجدد...")
                os.remove(session_file)
            
            client = TelegramClient(session_file, API_ID, API_HASH)
            await client.connect()
            
            if not await client.is_user_authorized():
                print("ارسال درخواست کد به شماره...")
                await client.send_code_request(PHONE_NUMBER)
                print("⏳ منتظر دریافت کد هستیم. این مرحله ممکن است چند دقیقه طول بکشد...")
                await asyncio.sleep(60)
                continue
            
            print("✅ ربات با موفقیت به تلگرام متصل شد!")
            while True:
                try:
                    await client.send_message(CHAT_ID, "میو")
                    print("پیام 'میو' ارسال شد.")
                except Exception as e:
                    print(f"خطا در ارسال پیام: {e}")
                await asyncio.sleep(INTERVAL_SECONDS)
                
        except sqlite3.DatabaseError:
            print("⚠️ خطای دیتابیس! فایل خراب است، حذف می‌شود و تلاش مجدد...")
            os.remove('session_mew.session')
            await asyncio.sleep(5)
        except Exception as e:
            print(f"خطای عمومی: {e}")
            await asyncio.sleep(60)

def run_async():
    asyncio.run(bot_loop())

if __name__ == '__main__':
    print("در حال راه‌اندازی ربات...")
    threading.Thread(target=run_async, daemon=True).start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
