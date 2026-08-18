import asyncio
import os
from telethon import TelegramClient

# متغیرهای محیطی
api_id = int(os.environ.get('API_ID', 0))
api_hash = os.environ.get('API_HASH', '')
phone = os.environ.get('PHONE_NUMBER', '')
chat_id = int(os.environ.get('CHAT_ID', 0))

INTERVAL_SECONDS = 280

if not api_id or not api_hash or not phone or not chat_id:
    print('❌ خطا: متغیرهای محیطی تنظیم نشده‌اند!')
    exit(1)

async def send_meow():
    client = TelegramClient('session_meow', api_id, api_hash)
    try:
        await client.start(phone=phone)
        print('✅ اتصال برقرار شد')
        await client.send_message(chat_id, 'میو')
        print('✅ پیام ارسال شد')
    except Exception as e:
        print(f'❌ خطا: {e}')
    finally:
        await client.disconnect()

async def main():
    print('🚀 ربات شروع به کار کرد.')
    while True:
        await send_meow()
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == '__main__':
    asyncio.run(main())