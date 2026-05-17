from telethon import TelegramClient, events
from openai import OpenAI
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

TELEGRAM_API_ID = os.getenv('api_id')
TELEGRAM_API_HASH = os.getenv('api_hash')
GROUP_ID = int(os.getenv('group_id'))
TOKEN_DEEPSEEK = os.getenv('token_deepseek')

client = TelegramClient('bet_placing_bot', TELEGRAM_API_ID, TELEGRAM_API_HASH)
deepseek = OpenAI(
    api_key=TOKEN_DEEPSEEK,
    base_url="https://api.deepseek.com"
)

async def ask_deepseek(question):
    response = deepseek.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

async def main():
    async with client:
        @client.on(events.NewMessage(chats=GROUP_ID))
        async def handler(event):
            message = event.message.text
            print(f"New message: {message}")

            answer = await ask_deepseek(message)
            print(f"DeepSeek answer: {answer}")

        await client.run_until_disconnected()

asyncio.run(main())