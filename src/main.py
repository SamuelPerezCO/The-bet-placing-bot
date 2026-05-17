from telethon import TelegramClient, events
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

TELEGRAM_API_ID = os.getenv('api_id')
TELEGRAM_API_HASH = os.getenv('api_hash')
GROUP_ID = int(os.getenv('group_id'))

client = TelegramClient('bet_placing_bot', TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def main():
    async with client:
        @client.on(events.NewMessage(chats=GROUP_ID))
        async def handler(event):
            print(f"New message: {event.message.text}")

        # async for msg in client.iter_messages(GROUP_ID, limit=100):
        #     print(msg.text)

asyncio.run(main())