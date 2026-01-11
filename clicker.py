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

@client.on(events.NewMessage(chats='@blurrr_dating_bot'))
async def handle_match_notification(event):
    # Проверяем: есть ли текст "У вас новый мэтч!" ИЛИ "У вас новый матч!"
    if ("У вас новый мэтч!" in event.raw_text or "У вас новый матч!" in event.raw_text) and event.message.reply_markup:
        try:
            print("[blurrr] Обнаружен мэтч. Нажимаю 'Посмотреть позже'...")
            await asyncio.sleep(1.0)
            # Кнопка "Посмотреть позже" — обычно вторая (индекс 1)
            await event.message.click(1)
            print("[blurrr] Успешно нажали 'Посмотреть позже'")
        except Exception as e:
            print(f"[blurrr] Ошибка при нажатии кнопки: {e}")

# ... остальные обработчики можно добавить позже ...

async def main():
    print("~ Кликер запущен ~")
    await client.start()
    print("✅ Готов. Жду сообщения от ботов...")
    await client.run_until_disconnected()

if __name__ == '__main__':

    asyncio.run(main())
