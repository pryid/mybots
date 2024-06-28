import os
import json
import logging
from random import choice, randint
from pyrogram import Client, filters
from pyrogram.types import Message
from constants import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID

# Настройка уровня логирования для Pyrogram
logging.getLogger('pyrogram').setLevel(logging.WARNING)

# Путь к файлу с ответами
musarskoy_id = 1473899765
admin_id = 768483882
responses_file = '/app/data/musarskoy/responses.json'
photo_folder = '/app/data/musarskoy/photo'

# Загрузка JSON-файла с ответами
try:
    with open(responses_file, "r") as file:
        data = json.load(file)
        responses = data["responses"]
except Exception as e:
    # Логирование ошибки в канал
    async def log_error_to_channel(client, message):
        await client.send_message(LOG_CHANNEL_ID, f"Error loading responses: {e}")
    responses = []

# Функция для обновления и перезагрузки ответов
def update_and_reload_responses(new_response):
    responses.append(new_response)
    try:
        with open(responses_file, "w") as file:
            json.dump({"responses": responses}, file, ensure_ascii=False, indent=4)
    except Exception as e:
        # Логирование ошибки в канал
        async def log_error_to_channel(client, message):
            await client.send_message(LOG_CHANNEL_ID, f"Error saving responses: {e}")

# Функция для отправки рандомных фото из папки
def send_random_photo():
    try:
        photos = os.listdir(photo_folder)
        if photos:
            photo = choice(photos)
            return os.path.join(photo_folder, photo)
        else:
            return None
    except Exception as e:
        # Логирование ошибки в канал
        async def log_error_to_channel(client, message):
            await client.send_message(LOG_CHANNEL_ID, f"Error listing photos: {e}")
        return None

# Создание клиента Pyrogram
app = Client("musarskoy", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Функция для сохранения фотографий пациента в папку
@app.on_message(filters.photo & (filters.user(musarskoy_id) | filters.user(admin_id)))
async def save_photo_from_user(client, message: Message):
    try:
        photo = message.photo
        file_id = photo.file_id
        save_path = os.path.join(photo_folder, f"{file_id}.jpg")
        await client.download_media(message, save_path)
        # Логирование успешного сохранения фото в канал
        await client.send_message(LOG_CHANNEL_ID, f"Photo saved to {save_path}")
    except Exception as e:
        # Логирование ошибки в канал
        await client.send_message(LOG_CHANNEL_ID, f"Error saving photo: {e}")

# Функции для проверки наличия ключевых слов в сообщении
def check_message_for_keywords(message_text):
    keywords = ["мусарской", "мусар", "мусор", "министр", "смешной","мотя", "матвей"]
    message_text = message_text.lower()  # Приводим текст сообщения к нижнему регистру
    for keyword in keywords:
        if keyword in message_text:
            return True
    return False

def check_message_for_keywords_photo(message_text):
    keywords = ["чмоня"]
    message_text = message_text.lower()
    for keyword in keywords:
        if keyword in message_text:
            return True
    return False

# Обработчик сообщений
@app.on_message(filters.text)
async def echo(client, message):
    # Проверка ID пользователя
    if message.from_user.id == musarskoy_id:
        update_and_reload_responses(message.text)
        #await message.reply("Ваше сообщение добавлено в список ответов.")
        await client.send_message(LOG_CHANNEL_ID, f"New response added: {message.text}")
    else:
        # Генерация случайного числа от 1 до 100
        random_number = randint(1, 100)

        # Проверка случайного числа для отправки фото
        if random_number == 2:
            photo_path = send_random_photo()
            if photo_path:
                await message.reply_photo(photo_path)
                await client.send_message(LOG_CHANNEL_ID, f"Sent random photo: {photo_path}")
            else:
                await message.reply("Фото отсутствуют.")
                await client.send_message(LOG_CHANNEL_ID, "No photos available to send.")
        # Проверка случайного числа для ответа без учета ключевых слов
        elif random_number == 1:
            response = choice(responses)
            await message.reply(response)
            await client.send_message(LOG_CHANNEL_ID, f"Sent random response: {response}")
        # Проверка для ответа с учетом ключевых слов    
        elif check_message_for_keywords(message.text):
            response = choice(responses)
            await message.reply(response)
            await client.send_message(LOG_CHANNEL_ID, f"Sent keyword-based response: {response}")
        # Проверка для ответа фото с учетом ключевых слов    
        elif check_message_for_keywords_photo(message.text):
            photo_path = send_random_photo()
            if photo_path:
                await message.reply_photo(photo_path)
                await client.send_message(LOG_CHANNEL_ID, f"Sent keyword-based photo: {photo_path}")
            else:
                await message.reply("Фото отсутствуют.")
                await client.send_message(LOG_CHANNEL_ID, "No photos available to send for keyword-based response.")
        elif message.reply_to_message and message.reply_to_message.from_user.id == client.me.id:
            # Если сообщение является ответом на сообщение бота
            response = choice(responses)
            await message.reply(response)
            await client.send_message(LOG_CHANNEL_ID, f"Replied to bot's message: {response}")

# Запуск бота
app.run()
