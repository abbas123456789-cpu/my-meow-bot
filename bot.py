import asyncio
import os
import sys
from telethon import TelegramClient

# ============================================
# اطلاعات از متغیرهای محیطی
# ============================================
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '')
CHAT_ID = int(os.environ.get('CHAT_ID', 0))

INTERVAL_SECONDS = 285  # ۴ دقیقه و ۴۵ ثانیه = ۲۸۵ ثانیه

# ============================================
# تابع چاپ با خروجی فوری
# ============================================
def print_flush(msg):
    """چاپ پیام با خروجی فوری"""
    print(msg)
    sys.stdout.flush()  #强制 خروجی فوری

# ============================================
# بررسی وجود اطلاعات
# ============================================
if not API_ID or not API_HASH or not PHONE_NUMBER or not CHAT_ID:
    print_flush('❌ خطا: متغیرهای محیطی تنظیم نشده‌اند!')
    print_flush('لطفاً متغیرهای زیر را تنظیم کنید:')
    print_flush('  - API_ID')
    print_flush('  - API_HASH')
    print_flush('  - PHONE_NUMBER')
    print_flush('  - CHAT_ID')
    exit(1)

print_flush('✅ متغیرهای محیطی با موفقیت خوانده شدند')

# ============================================
# تابع ارسال پیام
# ============================================
async def send_meow():
    """ارسال کلمه 'میو' به گروه مورد نظر"""
    print_flush('🔄 در حال اتصال به تلگرام...')
    client = TelegramClient('session_meow', API_ID, API_HASH)
    
    try:
        await client.start(phone=PHONE_NUMBER)
        print_flush('✅ اتصال به تلگرام برقرار شد')
        
        await client.send_message(CHAT_ID, 'میو')
        print_flush('✅ پیام "میو" با موفقیت ارسال شد')
        return True
        
    except Exception as e:
        print_flush(f'❌ خطا در ارسال: {e}')
        return False
    finally:
        await client.disconnect()
        print_flush('🔌 اتصال قطع شد')

# ============================================
# تابع اصلی
# ============================================
async def main():
    print_flush('🚀 ربات شروع به کار کرد.')
    print_flush(f'⏱️ هر {INTERVAL_SECONDS // 60} دقیقه و {INTERVAL_SECONDS % 60} ثانیه یکبار "میو" ارسال می‌شود.')
    print_flush('-' * 50)
    
    counter = 0
    while True:
        counter += 1
        print_flush(f'📤 ارسال شماره {counter}...')
        try:
            await send_meow()
        except Exception as e:
            print_flush(f'❌ خطای اصلی: {e}')
        print_flush(f'⏳ منتظر {INTERVAL_SECONDS} ثانیه تا ارسال بعدی...')
        await asyncio.sleep(INTERVAL_SECONDS)

# ============================================
# اجرا با مدیریت صحیح event loop
# ============================================
if __name__ == '__main__':
    try:
        print_flush('🔄 راه‌اندازی event loop...')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print_flush('\n🛑 ربات متوقف شد.')
    except Exception as e:
        print_flush(f'❌ خطای غیرمنتظره: {e}')
    finally:
        if 'loop' in locals():
            loop.close()
            print_flush('✅ Event loop بسته شد')
