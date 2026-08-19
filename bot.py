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
CODE = os.environ.get('CODE', None)  # کد تایید را از اینجا می‌خواند
INTERVAL_SECONDS = 280

print("✅ متغیرهای محیطی خوانده شدند.")

# تنظیم سرور وب
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
                print("📱 در حال ارسال درخواست کد تایید...")
                # ارسال درخواست کد
                await client.send_code_request(PHONE_NUMBER)
                
                # اگر CODE در محیط وجود دارد، آن را وارد کن
                if CODE:
                    print(f"🔑 کد تایید ({CODE}) در محیط پیدا شد! در حال ارسال به تلگرام...")
                    await client.sign_in(PHONE_NUMBER, CODE)
                    print("✅ لاگین موفقیت‌آمیز با کد تایید!")
                    await client.disconnect()
                    continue
                else:
                    print("⏳ منتظر کد تایید هستیم. کد را در متغیر محیطی CODE وارد کنید...")
                
                await client.disconnect()
                await asyncio.sleep(60)
                continue

            print("✅ ربات به تلگرام متصل شد!")
            while True:
                await client.send_message(CHAT_ID, "میو")
                print("📨 'میو' ارسال شد.")
                await asyncio.sleep(INTERVAL_SECONDS)
                
        except Exception as e:
            print(f"❌ خطا (تلاش مجدد در ۶۰ ثانیه): {e}")
            await asyncio.sleep(60)

threading.Thread(target=lambda: asyncio.run(bot_loop()), daemon=True).start()
port = int(os.environ.get('PORT', 10000))
app.run(host='0.0.0.0', port=port, debug=False)
