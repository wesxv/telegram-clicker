from telethon import TelegramClient, events, errors
import logging
import asyncio
import random
import os

logging.basicConfig(level=logging.INFO)

# Получаем API ключи из переменных окружения
api_id = int(os.getenv('API_ID', 123456))
api_hash = os.getenv('API_HASH', '0123456789abcdef0123456789abcdef')
# Список ботов
text_bots = ['@WombiBot', '@FaceAnonBot', '@FaceTop_Bot', '@bibinto_bot']

sleep_time = [2, 4, 6, 8]

client = TelegramClient('clicker_session', api_id, api_hash)

# === Обработчики ===

@client.on(events.NewMessage(chats=text_bots))
async def handle_text_bots(event):
    if event.message.media and not event.message.sticker and not event.message.animation:
        await asyncio.sleep(random.choice(sleep_time))
        try:
            await client.send_message(event.chat_id, str(random.choice([6, 7, 8])))
        except Exception as e:
            print(f'[Ошибка text_bots] {e}')

# ... остальные обработчики можно добавить позже ...

async def main():
    print("~ Кликер запущен ~")
    await client.start()
    print("✅ Готов. Жду сообщения от ботов...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())