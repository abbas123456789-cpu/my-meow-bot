import asyncio
import os
from telethon import TelegramClient

# ============================================
# اطلاعات از متغیرهای محیطی
# ============================================
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '')
CHAT_ID = int(os.environ.get('CHAT_ID', 0))

INTERVAL_SECONDS = 286

# ============================================
# بررسی وجود اطلاعات
# ============================================
if not API_ID or not API_HASH or not PHONE_NUMBER or not CHAT_ID:
    print('❌ خطا: متغیرهای محیطی تنظیم نشده‌اند!')
    print('لطفاً متغیرهای زیر را تنظیم کنید:')
    print('  - API_ID')
    print('  - API_HASH')
    print('  - PHONE_NUMBER')
    print('  - CHAT_ID')
    exit(1)

# ============================================
# تابع ارسال پیام
# ============================================
async def send_meow():
    """ارسال کلمه 'میو' به گروه مورد نظر"""
    client = TelegramClient('session_meow', API_ID, API_HASH)
    
    try:
        await client.start(phone=PHONE_NUMBER)
        print('✅ اتصال به تلگرام برقرار شد')
        await client.send_message(CHAT_ID, 'میو')
        print('✅ پیام "میو" با موفقیت ارسال شد')
        return True
    except Exception as e:
        print(f'❌ خطا در ارسال: {e}')
        return False
    finally:
        await client.disconnect()
        print('🔌 اتصال قطع شد')

# ============================================
# تابع اصلی
# ============================================
async def main():
    print('🚀 ربات شروع به کار کرد.')
    print(f'⏱️ هر {INTERVAL_SECONDS // 60} دقیقه و {INTERVAL_SECONDS % 60} ثانیه یکبار "میو" ارسال می‌شود.')
    print('-' * 50)
    
    while True:
        try:
            await send_meow()
        except Exception as e:
            print(f'❌ خطای اصلی: {e}')
        await asyncio.sleep(INTERVAL_SECONDS)

# ============================================
# اجرا با مدیریت صحیح event loop
# ============================================
if __name__ == '__main__':
    try:
        # ایجاد یک event loop جدید و اجرا
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('\n🛑 ربات متوقف شد.')
    finally:
        loop.close()
