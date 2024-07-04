import os
import json
import logging
import asyncio
from random import choice, randint
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from constants import API_ID, API_HASH, BOT_TOKEN, MUSAR_CHANNEL_ID

# Настройка уровня логирования для Pyrogram
logging.getLogger('pyrogram').setLevel(logging.WARNING)

# Путь к файлам с данными
musarskoy_id = 1473899765
admin_id = 768483882
responses_file = '/app/data/musarskoy/responses.json'
photos_file = '/app/data/musarskoy/photos.json'
voices_file = '/app/data/musarskoy/voices.json'
video_notes_file = '/app/data/musarskoy/video_notes.json'
videos_file = '/app/data/musarskoy/videos.json'
stickers_file = '/app/data/musarskoy/stickers.json'
music_file = '/app/data/musarskoy/music.json'
animations_file = '/app/data/musarskoy/animations.json'

# Загрузка JSON-файлов
def load_json_file(file_path, default_data):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        async def log_error_to_channel(client, message):
            await client.send_message(MUSAR_CHANNEL_ID, f"Error loading {file_path}: {e}")
        return default_data

responses_data = load_json_file(responses_file, {"responses": []})
responses = responses_data["responses"]

photos_data = load_json_file(photos_file, {"photo_ids": []})
photo_ids = photos_data.get("photo_ids", [])

voices_data = load_json_file(voices_file, {"voice_ids": []})
voice_ids = voices_data.get("voice_ids", [])

video_notes_data = load_json_file(video_notes_file, {"video_note_ids": []})
video_note_ids = video_notes_data.get("video_note_ids", [])

videos_data = load_json_file(videos_file, {"video_ids": []})
video_ids = videos_data.get("video_ids", [])

stickers_data = load_json_file(stickers_file, {"sticker_ids": []})
sticker_ids = stickers_data.get("sticker_ids", [])

music_data = load_json_file(music_file, {"music_ids": []})
music_ids = music_data.get("music_ids", [])

animations_data = load_json_file(animations_file, {"animation_ids": []})
animation_ids = animations_data.get("animation_ids", [])

# Функция для обновления и перезагрузки JSON-файлов
def update_and_reload_json_file(file_path, data):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        async def log_error_to_channel(client, message):
            await client.send_message(MUSAR_CHANNEL_ID, f"Error saving {file_path}: {e}")

# Функции для обновления данных
def update_and_reload_responses(new_response):
    responses.append(new_response)
    update_and_reload_json_file(responses_file, {"responses": responses})

def update_and_reload_photo_ids(new_photo_id):
    photo_ids.append(new_photo_id)
    update_and_reload_json_file(photos_file, {"photo_ids": photo_ids})

def update_and_reload_voice_ids(new_voice_id):
    voice_ids.append(new_voice_id)
    update_and_reload_json_file(voices_file, {"voice_ids": voice_ids})

def update_and_reload_video_note_ids(new_video_note_id):
    video_note_ids.append(new_video_note_id)
    update_and_reload_json_file(video_notes_file, {"video_note_ids": video_note_ids})

def update_and_reload_video_ids(new_video_id):
    video_ids.append(new_video_id)
    update_and_reload_json_file(videos_file, {"video_ids": video_ids})

def update_and_reload_sticker_ids(new_sticker_id):
    sticker_ids.append(new_sticker_id)
    update_and_reload_json_file(stickers_file, {"sticker_ids": sticker_ids})

def update_and_reload_music_ids(new_music_id):
    music_ids.append(new_music_id)
    update_and_reload_json_file(music_file, {"music_ids": music_ids})

def update_and_reload_animation_ids(new_animation_id):
    animation_ids.append(new_animation_id)
    update_and_reload_json_file(animations_file, {"animation_ids": animation_ids})

# Функции для отправки рандомных данных
async def send_random_item(client, message, item_list, chat_action, log_action, no_items_message):
    try:
        if item_list:
            item_id = choice(item_list)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_chat_action(message.chat.id, chat_action)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_cached_media(message.chat.id, item_id, reply_to_message_id=message.id)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(MUSAR_CHANNEL_ID, f"{log_action}: {item_id}")
        else:
            await message.reply(no_items_message)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(MUSAR_CHANNEL_ID, f"No {log_action} available to send.")
    except Exception as e:
        await client.send_message(MUSAR_CHANNEL_ID, f"Error selecting {log_action}: {e}")

# Создание клиента Pyrogram
app = Client("musarskoy", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Функция для сохранения file_id медиафайлов пациента
@app.on_message(filters.photo & (filters.user(musarskoy_id) | filters.user(admin_id)))
async def save_photo_from_user(client, message: Message):
    try:
        photo = message.photo
        file_id = photo.file_id
        update_and_reload_photo_ids(file_id)
        await client.send_cached_media(MUSAR_CHANNEL_ID, file_id, caption=f"Saved new #photo {file_id}")
        if message.caption:
            update_and_reload_responses(message.caption)
            await client.send_message(MUSAR_CHANNEL_ID, f"Photo caption added as response: {message.caption}")
    except Exception as e:
        await client.send_message(MUSAR_CHANNEL_ID, f"Error saving photo ID: {e}")

@app.on_message(filters.voice & (filters.user(musarskoy_id) | filters.user(admin_id)))
async def save_voice_from_user(client, message: Message):
    try:
        voice = message.voice
        file_id = voice.file_id
        update_and_reload_voice_ids(file_id)
        await client.send_cached_media(MUSAR_CHANNEL_ID, file_id, caption=f"Saved new #voice {file_id}")
        if message.caption:
            update_and_reload_responses(message.caption)
            await client.send_message(MUSAR_CHANNEL_ID, f"Voice caption added as response: {message.caption}")
    except Exception as e:
        await client.send_message(MUSAR_CHANNEL_ID, f"Error saving voice ID: {e}")

@app.on_message(filters.video_note & (filters.user(musarskoy_id) | filters.user(admin_id)))
async def save_video_note_from_user(client, message: Message):
    try:
        video_note = message.video_note
        file_id = video_note.file_id
        update_and_reload_video_note_ids(file_id)
        await client.send_cached_media(MUSAR_CHANNEL_ID, file_id, caption=f"Saved new #videonote {file_id}")
        if message.caption:
            update_and_reload_responses(message.caption)
            await client.send_message(MUSAR_CHANNEL_ID, f"Video note caption added as response: {message.caption}")
    except Exception as e:
        await client.send_message(MUSAR_CHANNEL_ID, f"Error saving video note ID: {e}")

@app.on_message(filters.video & (filters.user(musarskoy_id) | filters.user(admin_id)))
async def save_video_from_user(client, message: Message):
    try:
        video = message.video
        file_id = video.file_id
        update_and_reload_video_ids(file_id)
        await client.send_cached_media(MUSAR_CHANNEL_ID, file_id, caption=f"Saved new #video {file_id}")
        if message.caption:
            update_and_reload_responses(message.caption)
            await client.send_message(MUSAR_CHANNEL_ID, f"Video caption added as response: {message.caption}")
    except Exception as e:
        await client.send_message(MUSAR_CHANNEL_ID, f"Error saving video ID: {e}")

@app.on_message(filters.sticker & (filters.user(musarskoy_id) | filters.user(admin_id)))
async def save_sticker_from_user(client, message: Message):
    try:
        sticker = message.sticker
        file_id = sticker.file_id
        update_and_reload_sticker_ids(file_id)
        await client.send_message(MUSAR_CHANNEL_ID, f"Sticker ID saved: {file_id}")
        await client.send_sticker(MUSAR_CHANNEL_ID, file_id)
        if message.caption:
            update_and_reload_responses(message.caption)
            await client.send_message(MUSAR_CHANNEL_ID, f"Sticker caption added as response: {message.caption}")
    except Exception as e:
        await client.send_message(MUSAR_CHANNEL_ID, f"Error saving sticker ID: {e}")

@app.on_message(filters.audio & (filters.user(musarskoy_id) | filters.user(admin_id)))
async def save_music_from_user(client, message: Message):
    try:
        music = message.audio
        file_id = music.file_id
        update_and_reload_music_ids(file_id)
        await client.send_cached_media(MUSAR_CHANNEL_ID, file_id, caption=f"Saved new #music {file_id}")
        if message.caption:
            update_and_reload_responses(message.caption)
            await client.send_message(MUSAR_CHANNEL_ID, f"Music caption added as response: {message.caption}")
    except Exception as e:
        await client.send_message(MUSAR_CHANNEL_ID, f"Error saving music ID: {e}")

@app.on_message(filters.animation & (filters.user(musarskoy_id) | filters.user(admin_id)))
async def save_animation_from_user(client, message: Message):
    try:
        animation = message.animation
        file_id = animation.file_id
        update_and_reload_animation_ids(file_id)
        await client.send_cached_media(MUSAR_CHANNEL_ID, file_id, caption=f"Saved new #animation {file_id}")
        if message.caption:
            update_and_reload_responses(message.caption)
            await client.send_message(MUSAR_CHANNEL_ID, f"Animation caption added as response: {message.caption}")
    except Exception as e:
        await client.send_message(MUSAR_CHANNEL_ID, f"Error saving animation ID: {e}")

# Функции для проверки наличия ключевых слов в сообщении
def check_message_for_keywords(message_text, keywords):
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
        if message.caption:
            update_and_reload_responses(message.caption)
            await client.send_message(MUSAR_CHANNEL_ID, f"New response added from caption: {message.caption}")
        else:
            update_and_reload_responses(message.text)
            await client.send_message(MUSAR_CHANNEL_ID, f"New response added: {message.text}")
        await asyncio.sleep(1)  # Задержка 1 секунда
    else:
        # Генерация случайного числа от 1 до 100
        random_number = randint(1, 300)

        # Проверка случайного числа для отправки различных типов медиа
        if random_number == 2:
            await send_random_item(client, message, photo_ids, ChatAction.UPLOAD_PHOTO, "Sent random photo", "Фото отсутствуют.")
        elif random_number == 3:
            await send_random_item(client, message, voice_ids, ChatAction.RECORD_AUDIO, "Sent random voice", "Голосовые сообщения отсутствуют.")
        elif random_number == 4:
            await send_random_item(client, message, video_note_ids, ChatAction.RECORD_VIDEO_NOTE, "Sent random video note", "Видеозаметки отсутствуют.")
        elif random_number == 5:
            await send_random_item(client, message, video_ids, ChatAction.UPLOAD_VIDEO, "Sent random video", "Видео отсутствуют.")
        elif random_number == 6:
            await send_random_item(client, message, sticker_ids, ChatAction.CHOOSE_STICKER, "Sent random sticker", "Стикеры отсутствуют.")
        elif random_number == 7:
            await send_random_item(client, message, music_ids, ChatAction.UPLOAD_AUDIO, "Sent random music", "Музыкальные сообщения отсутствуют.")
        elif random_number == 8:
            await send_random_item(client, message, animation_ids, ChatAction.UPLOAD_PHOTO, "Sent random animation", "Анимации отсутствуют.")
        elif random_number == 1 or check_message_for_keywords(message.text, ["мусар", "мусор", "министр", "смешной", "мотя", "матвей"]):
            response = choice(responses)
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await message.reply(response)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(MUSAR_CHANNEL_ID, f"Sent response: {response}")
        elif check_message_for_keywords(message.text, ["чмоня"]):
            await send_random_item(client, message, photo_ids, ChatAction.UPLOAD_PHOTO, "Sent random photo", "Фото отсутствуют.")
        elif check_message_for_keywords(message.text, ["помяукай"]):
            await send_random_item(client, message, voice_ids, ChatAction.RECORD_AUDIO, "Sent random voice", "Голосовые сообщения отсутствуют.")
        elif check_message_for_keywords(message.text, ["блинчик"]):
            await send_random_item(client, message, video_note_ids, ChatAction.RECORD_VIDEO_NOTE, "Sent random video note", "Видеозаметки отсутствуют.")
        elif check_message_for_keywords(message.text, ["видярик"]):
            await send_random_item(client, message, video_ids, ChatAction.UPLOAD_VIDEO, "Sent random video", "Видео отсутствуют.")
        elif check_message_for_keywords(message.text, ["стикос"]):
            await send_random_item(client, message, sticker_ids, ChatAction.CHOOSE_STICKER, "Sent random sticker", "Стикеры отсутствуют.")
        elif check_message_for_keywords(message.text, ["музло"]):
            await send_random_item(client, message, music_ids, ChatAction.UPLOAD_DOCUMENT, "Sent random music", "Музыкальные сообщения отсутствуют.")
        elif check_message_for_keywords(message.text, ["дрыга"]):
            await send_random_item(client, message, animation_ids, ChatAction.UPLOAD_VIDEO, "Sent random animation", "Анимации отсутствуют.")
        elif check_message_for_keywords(message.text, ["шлюха", "проститутка"]):
            await client.send_reaction(message.chat.id, message.id, emoji="👍", big=True)
        elif message.reply_to_message and message.reply_to_message.from_user.id == client.me.id:
            response = choice(responses)
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await message.reply(response)
            await asyncio.sleep(1)  # Задержка 1 секунда
            await client.send_message(MUSAR_CHANNEL_ID, f"Replied to bot's message: {response}")

# Запуск бота
app.run()