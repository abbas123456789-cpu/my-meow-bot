import asyncio
import os
from telethon import TelegramClient
from flask import Flask

# دریافت متغیرهای محیطی
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '')
CHAT_ID = int(os.environ.get('CHAT_ID', 0))
INTERVAL_SECONDS = 286

# بررسی وجود متغیرها
if not API_ID or not API_HASH or not PHONE_NUMBER or not CHAT_ID:
    print("خطا: متغیرهای محیطی تنظیم نشده‌اند.")
    exit(1)

# تنظیم سرور وب (این بخش برنامه را برای Render روشن نگه می‌دارد)
app = Flask(__name__)
@app.route('/')
def home():
    return "ربات در حال کار است!"

# بخش اصلی ربات
async def main():
    client = TelegramClient('session_mew', API_ID, API_HASH)
    try:
        await client.start(PHONE_NUMBER)
        print("ربات با موفقیت متصل شد و در حال کار است!")
        while True:
            await client.send_message(CHAT_ID, "میو")
            print("پیام 'میو' ارسال شد.")
            await asyncio.sleep(INTERVAL_SECONDS)
    except Exception as e:
        print(f"خطای ربات: {e}")

if __name__ == '__main__':
    # این قسمت هم سرور وب را اجرا می‌کند، هم ربات را (بدون نیاز به threading)
    from threading import Thread
    Thread(target=lambda: asyncio.run(main())).start()
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
