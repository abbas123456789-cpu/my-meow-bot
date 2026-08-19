import asyncio
import os
from telethon import TelegramClient
from flask import Flask
import threading

API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '')
CHAT_ID = int(os.environ.get('CHAT_ID', 0))
INTERVAL_SECONDS = 280

print("✅ متغیرهای محیطی خوانده شدند.")
print("⏳ در حال راه‌اندازی...")

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
                print("📱 در حال ارسال درخواست کد تایید به شماره شما...")
                await client.send_code_request(PHONE_NUMBER)
                print("✅ درخواست کد ارسال شد. کد باید به پیامک شما بیاید.")
                print("⏳ منتظر می‌مانیم تا آن کد را در Render وارد کنید...")
                await client.disconnect()
                await asyncio.sleep(60)
                continue

            print("✅ ربات به تلگرام متصل شد!")
            while True:
                await client.send_message(CHAT_ID, "میو")
                print("📨 'میو' ارسال شد.")
                await asyncio.sleep(INTERVAL_SECONDS)
        except Exception as e:
            print(f"❌ خطا: {e}")
            await asyncio.sleep(60)

threading.Thread(target=lambda: asyncio.run(bot_loop()), daemon=True).start()
port = int(os.environ.get('PORT', 10000))
app.run(host='0.0.0.0', port=port, debug=False)
