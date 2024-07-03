import os
import json
import logging
import asyncio
from random import choice, randint
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from constants import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID

# Настройка уровня логирования для Pyrogram
logging.getLogger('pyrogram').setLevel(logging.WARNING)

# Путь к файлам с данными
musarskoy_id = 1473899765
admin_id = 768483882
responses_file = '/app/data/musarskoy/responses.json'
photos_file = '/app/data/musarskoy/photos.json'
voices_file = '/app/data/musarskoy/voices.json'
video_notes_file = '/app/data/musarskoy/video_notes.json'

# Загрузка JSON-файлов
try:
    with open(responses_file, "r") as file:
        data = json.load(file)
        responses = data["responses"]
except Exception as e:
    async def log_error_to_channel(client, message):
        await client.send_message(LOG_CHANNEL_ID, f"Error loading responses: {e}")
    responses = []

try:
    with open(photos_file, "r") as file:
        data = json.load(file)
        photo_ids = data.get("photo_ids", [])
except Exception as e:
    async def log_error_to_channel(client, message):
        await client.send_message(LOG_CHANNEL_ID, f"Error loading photo_ids: {e}")
    photo_ids = []

try:
    with open(voices_file, "r") as file:
        data = json.load(file)
        voice_ids = data.get("voice_ids", [])
except Exception as e:
    async def log_error_to_channel(client, message):
        await client.send_message(LOG_CHANNEL_ID, f"Error loading voice_ids: {e}")
    voice_ids = []

try:
    with open(video_notes_file, "r") as file:
        data = json.load(file)
        video_note_ids = data.get("video_note_ids", [])
except Exception as e:
    async def log_error_to_channel(client, message):
        await client.send_message(LOG_CHANNEL_ID, f"Error loading video_note_ids: {e}")
    video_note_ids = []

# Функция для обновления и перезагрузки ответов
def update_and_reload_responses(new_response):
    responses.append(new_response)
    try:
        with open(responses_file, "w") as file:
            json.dump({"responses": responses}, file, ensure_ascii=False, indent=4)
    except Exception as e:
        async def log_error_to_channel(client, message):
            await client.send_message(LOG_CHANNEL_ID, f"Error saving responses: {e}")

# Функция для обновления и перезагрузки photo_ids
def update_and_reload_photo_ids(new_photo_id):
    photo_ids.append(new_photo_id)
    try:
        with open(photos_file, "w") as file:
            json.dump({"photo_ids": photo_ids}, file, ensure_ascii=False, indent=4)
    except Exception as e:
        async def log_error_to_channel(client, message):
            await client.send_message(LOG_CHANNEL_ID, f"Error saving photo_ids: {e}")

# Функция для обновления и перезагрузки voice_ids
def update_and_reload_voice_ids(new_voice_id):
    voice_ids.append(new_voice_id)
    try:
        with open(voices_file, "w") as file:
            json.dump({"voice_ids": voice_ids}, file, ensure_ascii=False, indent=4)
    except Exception as e:
        async def log_error_to_channel(client, message):
            await client.send_message(LOG_CHANNEL_ID, f"Error saving voice_ids: {e}")

# Функция для обновления и перезагрузки video_note_ids
def update_and_reload_video_note_ids(new_video_note_id):
    video_note_ids.append(new_video_note_id)
    try:
        with open(video_notes_file, "w") as file:
            json.dump({"video_note_ids": video_note_ids}, file, ensure_ascii=False, indent=4)
    except Exception as e:
        async def log_error_to_channel(client, message):
            await client.send_message(LOG_CHANNEL_ID, f"Error saving video_note_ids: {e}")

# Функция для отправки рандомных фото из списка photo_ids
async def send_random_photo_id(client, message):
    try:
        if photo_ids:
            photo_id = choice(photo_ids)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_cached_media(message.chat.id, photo_id, reply_to_message_id=message.id)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(LOG_CHANNEL_ID, f"Sent random photo: {photo_id}")
        else:
            await message.reply("Фото отсутствуют.")
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(LOG_CHANNEL_ID, "No photo IDs available to send.")
    except Exception as e:
        await client.send_message(LOG_CHANNEL_ID, f"Error selecting random photo_id: {e}")

# Функция для отправки рандомных голосовых сообщений из списка voice_ids
async def send_random_voice_id(client, message):
    try:
        if voice_ids:
            voice_id = choice(voice_ids)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_chat_action(message.chat.id, ChatAction.RECORD_AUDIO)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_cached_media(message.chat.id, voice_id, reply_to_message_id=message.id)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(LOG_CHANNEL_ID, f"Sent random voice: {voice_id}")
        else:
            await message.reply("Голосовые сообщения отсутствуют.")
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(LOG_CHANNEL_ID, "No voice IDs available to send.")
    except Exception as e:
        await client.send_message(LOG_CHANNEL_ID, f"Error selecting random voice_id: {e}")

# Функция для отправки рандомных видеозаметок из списка video_note_ids
async def send_random_video_note_id(client, message):
    try:
        if video_note_ids:
            video_note_id = choice(video_note_ids)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_chat_action(message.chat.id, ChatAction.RECORD_VIDEO_NOTE)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_cached_media(message.chat.id, video_note_id, reply_to_message_id=message.id)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(LOG_CHANNEL_ID, f"Sent random video note: {video_note_id}")
        else:
            await message.reply("Видеозаметки отсутствуют.")
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(LOG_CHANNEL_ID, "No video note IDs available to send.")
    except Exception as e:
        await client.send_message(LOG_CHANNEL_ID, f"Error selecting random video_note_id: {e}")

# Создание клиента Pyrogram
app = Client("musarskoy", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Функция для сохранения file_id фотографий пациента
@app.on_message(filters.photo & (filters.user(musarskoy_id) | filters.user(admin_id)))
async def save_photo_from_user(client, message: Message):
    try:
        photo = message.photo
        file_id = photo.file_id
        update_and_reload_photo_ids(file_id)
        await client.send_message(LOG_CHANNEL_ID, f"Photo ID saved: {file_id}")
    except Exception as e:
        await client.send_message(LOG_CHANNEL_ID, f"Error saving photo ID: {e}")

# Функция для сохранения file_id голосовых сообщений пациента
@app.on_message(filters.voice & (filters.user(musarskoy_id) | filters.user(admin_id)))
async def save_voice_from_user(client, message: Message):
    try:
        voice = message.voice
        file_id = voice.file_id
        update_and_reload_voice_ids(file_id)
        await client.send_message(LOG_CHANNEL_ID, f"Voice ID saved: {file_id}")
    except Exception as e:
        await client.send_message(LOG_CHANNEL_ID, f"Error saving voice ID: {e}")

# Функция для сохранения file_id видеозаметок пациента
@app.on_message(filters.video_note & (filters.user(musarskoy_id) | filters.user(admin_id)))
async def save_video_note_from_user(client, message: Message):
    try:
        video_note = message.video_note
        file_id = video_note.file_id
        update_and_reload_video_note_ids(file_id)
        await client.send_message(LOG_CHANNEL_ID, f"Video note ID saved: {file_id}")
    except Exception as e:
        await client.send_message(LOG_CHANNEL_ID, f"Error saving video note ID: {e}")

# Функции для проверки наличия ключевых слов в сообщении
def check_message_for_keywords(message_text):
    keywords = ["мусар", "мусор", "министр", "смешной", "мотя", "матвей"]
    message_text = message_text.lower()
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

def check_message_for_keywords_voice(message_text):
    keywords = ["чайник"]
    message_text = message_text.lower()
    for keyword in keywords:
        if keyword in message_text:
            return True
    return False

def check_message_for_keywords_video_note(message_text):
    keywords = ["круг"]
    message_text = message_text.lower()
    for keyword in keywords:
        if keyword in message_text:
            return True
    return False

def check_message_for_keywords_reaction(message_text):
    keywords = ["шлюха", "проститутка"]
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
        await client.send_message(LOG_CHANNEL_ID, f"New response added: {message.text}")
        await asyncio.sleep(1)  # Задержка 1 секунда
    else:
        # Генерация случайного числа от 1 до 100
        random_number = randint(1, 100)

        # Проверка случайного числа для отправки фото
        if random_number == 2:
            await send_random_photo_id(client, message)
        # Проверка случайного числа для отправки голосового сообщения
        elif random_number == 3:
            await send_random_voice_id(client, message)
        # Проверка случайного числа для отправки видеозаметки
        elif random_number == 4:
            await send_random_video_note_id(client, message)
        # Проверка случайного числа для ответа без учета ключевых слов
        elif random_number == 1:
            response = choice(responses)
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await message.reply(response)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(LOG_CHANNEL_ID, f"Sent random response: {response}")
        # Проверка для ответа с учетом ключевых слов    
        elif check_message_for_keywords(message.text):
            response = choice(responses)
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await message.reply(response)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(LOG_CHANNEL_ID, f"Sent keyword-based response: {response}")
        # Проверка для ответа фото с учетом ключевых слов    
        elif check_message_for_keywords_photo(message.text):
            await send_random_photo_id(client, message)
        # Проверка для ответа голосовым сообщением с учетом ключевых слов
        elif check_message_for_keywords_voice(message.text):
            await send_random_voice_id(client, message)
        # Проверка для ответа видеозаметкой с учетом ключевых слов
        elif check_message_for_keywords_video_note(message.text):
            await send_random_video_note_id(client, message)
        # Проверка для реакции на сообщения с определенными ключевыми словами
        elif check_message_for_keywords_reaction(message.text):
            await client.send_reaction(message.chat.id, message.id, emoji="👍", big=True)
        # Проверка для ответа на сообщения, которые являются ответом на сообщение бота
        elif message.reply_to_message and message.reply_to_message.from_user.id == client.me.id:
            response = choice(responses)
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await message.reply(response)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(LOG_CHANNEL_ID, f"Replied to bot's message: {response}")

# Запуск бота
app.run()