from telethon import TelegramClient, events
from dotenv import load_dotenv
from openai import OpenAI
import asyncio
import easyocr
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

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

async def place_bet(bet_details):
    pass

async def extract_text(message):
    """extract the text from the image and send it to deepseek to get 
        the answer and then place the bet"""
    reader = easyocr.Reader(['en' , 'es'])

    result = reader.readtext(message)

    for detection in result:
        print(detection[1])  # This will print the detected text

async def download_image(event):
    message = event.message
    if message.photo or (message.document and message.document.mime_type.startswith("image/")):
        path = await event.download_media(file="downloads/")
        print("Image downloaded to:", path)
        return path
    return None

async def ask_deepseek(question):
    """Falta agregarle el contexto de que va a hacer y como debe de responder para que la funcion que 
    hace la apuesta sea mas facil de implementar"""
    response = deepseek.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

async def main():
    async with client:
        # @client.on(events.NewMessage(chats=GROUP_ID))
        @client.on(events.NewMessage(chats=-5271750467))
        async def handler(event):
            message = event.message

            downloaded = await download_image(event)
            if downloaded:
                return

            if message.text:
                print(f"New message: {message.text}")
                answer = await ask_deepseek(message.text)
                print(f"DeepSeek answer: {answer}")

        await client.run_until_disconnected()

asyncio.run(main())