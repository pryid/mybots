import json
import asyncio
from pyrogram import Client, errors
API_ID=26121547
API_HASH=""
BOT_TOKEN=""

# ID канала, в который будут отправляться медиафайлы
CHANNEL_ID = -1002152305595

# Путь к файлам с данными
responses_file = 'responses.json'
photos_file = 'photos.json'
voices_file = 'voices.json'
video_notes_file = 'video_notes.json'
videos_file = 'videos.json'
stickers_file = 'stickers.json'
music_file = 'music.json'
animations_file = 'animations.json'

# Загрузка JSON-файлов
def load_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}

# Функция для отправки файла в канал
async def send_file(client, file_id, caption):
    while True:
        try:
            await client.send_cached_media(CHANNEL_ID, file_id, caption=caption)
            await asyncio.sleep(2)  # Задержка 2 секунды между отправками
            break
        except errors.FloodWait as e:
            print(f"Flood wait: {e.value} seconds")
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Error sending file {file_id}: {e}")
            break

# Функция для отправки всех файлов из JSON-файлов
async def send_all_files(client):
    json_files = [
        (photos_file, "photo_ids", "#photo"),
        (voices_file, "voice_ids", "#voice"),
        (video_notes_file, "video_note_ids", "#videonote"),
        (videos_file, "video_ids", "#video"),
        (stickers_file, "sticker_ids", "#sticker"),
        (music_file, "music_ids", "#music"),
        (animations_file, "animation_ids", "#animation")
    ]

    for file_path, key, tag in json_files:
        data = load_json_file(file_path)
        file_ids = data.get(key, [])
        for file_id in file_ids:
            caption = f"Saved new {tag} {file_id}"
            await send_file(client, file_id, caption)

# Создание клиента Pyrogram
app = Client("musarskoy", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Запуск клиента и отправка файлов
async def main():
    await app.start()
    await send_all_files(app)
    await app.stop()

# Создание и запуск новой петли событий
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
