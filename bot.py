import asyncio
import os
from telethon import TelegramClient, functions
from flask import Flask
import threading

# دریافت متغیرهای محیطی
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '')
CHAT_ID = int(os.environ.get('CHAT_ID', 0))
INTERVAL_SECONDS = 286

print("متغیرهای محیطی با موفقیت خوانده شدند.")

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
            
            # بررسی میکنیم که آیا لاگین هستیم یا نه (این کار باعث نمیشود برنامه منتظر کد بماند)
            if not await client.is_user_authorized():
                print("اکانت هنوز لاگین نشده. در حال تلاش برای ارسال درخواست کد...")
                # ارسال درخواست کد تایید به تلگرام (اما منتظر وارد کردن کد نمی‌شویم!)
                await client(functions.auth.SendCodeRequest(
                    phone_number=PHONE_NUMBER,
                    api_id=API_ID,
                    api_hash=API_HASH
                ))
                print("درخواست کد تایید ارسال شد. برنامه متوقف نمی‌شود. تلاش دوباره در ۱ دقیقه...")
                await client.disconnect()
                await asyncio.sleep(60)
                continue

            print("ربات با موفقیت به تلگرام متصل شد! (اعتبار سنجی شده)")
            
            # حلقه اصلی ارسال پیام
            while True:
                try:
                    await client.send_message(CHAT_ID, "میو")
                    print("پیام 'میو' ارسال شد.")
                except Exception as e:
                    print(f"خطا در ارسال پیام: {e}")
                await asyncio.sleep(INTERVAL_SECONDS)
                
        except Exception as e:
            print(f"خطای کلی در حلقه ربات (تلاش مجدد): {e}")
            await asyncio.sleep(60)

def run_async():
    asyncio.run(bot_loop())

if __name__ == '__main__':
    print("در حال راه‌اندازی ربات...")
    bot_thread = threading.Thread(target=run_async, daemon=True)
    bot_thread.start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
