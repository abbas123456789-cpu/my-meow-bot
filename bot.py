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

# بررسی وجود متغیرها
if not API_ID or not API_HASH or not PHONE_NUMBER or not CHAT_ID:
    print("خطا: متغیرهای محیطی تنظیم نشده‌اند.")
    exit(1)

app = Flask(__name__)

@app.route('/')
def home():
    return "ربات تلگرام در حال کار است! 🚀"

# ساخت کلاینت
client = TelegramClient('session_mew', API_ID, API_HASH)

async def send_mew():
    try:
        await client.send_message(CHAT_ID, "میو")
        print(f"پیام 'میو' ارسال شد.")
    except Exception as e:
        print(f"خطا در ارسال پیام: {e}")

async def bot_main():
    try:
        # اینجا بدون نیاز به رمز ۲FA سعی می‌کند لاگین کند
        await client.start(PHONE_NUMBER) 
        print("ربات با موفقیت به تلگرام متصل شد!")
        
        while True:
            await send_mew()
            await asyncio.sleep(INTERVAL_SECONDS)
            
    except Exception as e:
        print(f"خطای اتصال: {e}. تلاش مجدد بعد از ۶۰ ثانیه...")
        await asyncio.sleep(60)
        await bot_main() # دوباره امتحان کن

def run_bot_in_thread():
    asyncio.run(bot_main())

if __name__ == '__main__':
    print("در حال راه‌اندازی ربات...")
    
    bot_thread = threading.Thread(target=run_bot_in_thread, daemon=True)
    bot_thread.start()
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
