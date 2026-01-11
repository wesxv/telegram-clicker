from telethon import TelegramClient, events, errors
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import logging
import asyncio
import random
import os

logging.basicConfig(level=logging.INFO)

# Получаем API ключи из переменных окружения
api_id = int(os.getenv('API_ID', 123456))
api_hash = os.getenv('API_HASH', '0123456789abcdef0123456789abcdef')

# Список ботов с текстовой оценкой
text_bots = ['@WombiBot', '@FaceAnonBot', '@FaceTop_Bot', '@bibinto_bot']

sleep_time = [2, 4, 6, 8]

client = TelegramClient('clicker_session', api_id, api_hash)

# === ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ: проверка медиа ===
def is_media_message(message):
    """Возвращает True, если сообщение содержит фото или видео."""
    if message.photo:
        return True
    if message.document:
        mime = getattr(message.document, 'mime_type', '') or ''
        return mime.startswith('video/') or getattr(message.document, 'video', False)
    return False

# === ОБРАБОТЧИКИ ===

# 1. Боты с текстовой оценкой
@client.on(events.NewMessage(chats=text_bots))
async def handle_text_bots(event):
    if is_media_message(event.message):
        await asyncio.sleep(random.choice(sleep_time))
        try:
            await client.send_message(event.chat_id, str(random.choice([6, 7, 8])))
        except errors.FloodWaitError as e:
            print(f'[ФЛУД text_bots] Ждём {e.seconds} секунд')
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f'[Ошибка text_bots] {e}')

# 2. @blurrr_dating_bot — анкеты (фото/видео)
@client.on(events.NewMessage(chats='@blurrr_dating_bot'))
async def handle_blurrr(event):
    if is_media_message(event.message) and event.message.reply_markup:
        try:
            print("[blurrr] Получено фото/видео. Нажимаю ❤️ (кнопка 2)")
            await asyncio.sleep(random.uniform(2.0, 5.0))
            await event.message.click(2)
            print("[blurrr] Успешно!")
        except errors.FloodWaitError as e:
            print(f'[ФЛУД blurrr] Ждём {e.seconds} секунд')
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f'[Ошибка blurrr] {e}')

# 3. @blurrr_dating_bot — уведомления о мэтче
@client.on(events.NewMessage(chats='@blurrr_dating_bot'))
async def handle_match_notification(event):
    if ("У вас новый мэтч!" in event.raw_text or "У вас новый матч!" in event.raw_text) and event.message.reply_markup:
        try:
            print("[blurrr] Обнаружен мэтч. Нажимаю 'Посмотреть позже'...")
            await asyncio.sleep(1.0)
            await event.message.click(1)  # "Посмотреть позже" — вторая кнопка
            print("[blurrr] Успешно нажали 'Посмотреть позже'")
        except Exception as e:
            print(f"[blurrr] Ошибка при нажатии кнопки: {e}")

# === ЗАПУСК ===
async def main():
    print("~ Кликер запущен ~")
    await client.start()
    print("✅ Готов. Жду сообщения от ботов...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
