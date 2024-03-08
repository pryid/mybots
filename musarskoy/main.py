# Стандартные библиотеки Python
import os
import json
from random import choice, randint
from time import sleep

# Внешние библиотеки
from pyrogram import Client, filters

# Локальные импорты
from constants import API_ID, API_HASH, BOT_TOKEN

# Путь к файлу с ответами

responses_file = '/app/data/musarskoy/responses.json'
photo_folder = '/app/data/musarskoy/photo'

# Загрузка JSON-файла с ответами
with open(responses_file, "r") as file:
    data = json.load(file)
    responses = data["responses"]

# Функция для обновления и перезагрузки ответов
def update_and_reload_responses(new_response):
    responses.append(new_response)
    with open(responses_file, "w") as file:
        json.dump({"responses": responses}, file, ensure_ascii=False, indent=4)

#Функция для отправки рандомных фото из папки
def send_random_photo():
    photos = os.listdir(photo_folder)
    if photos:
        photo = choice(photos)
        return os.path.join(photo_folder, photo)
    else:
        return None

# Создание клиента Pyrogram
app = Client("musarskoy", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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
    if message.from_user.id == 1473899765:
        update_and_reload_responses(message.text)
        #await message.reply("Ваше сообщение добавлено в список ответов.")
    else:
        # Генерация случайного числа от 1 до 100
        random_number = randint(1, 100)

        # Проверка случайного числа для отправки фото
        if random_number == 2:
            photo_path = send_random_photo()
            if photo_path:
                await client.send_photo(chat_id=message.chat.id, photo=photo_path, reply_to_message_id=message.message_id)
            else:
                await message.reply("Фото отсутствуют.")
        # Проверка случайного числа для ответа без учета ключевых слов
        if random_number == 1:
            response = choice(responses)
            await message.reply(response)
        # Проверка для ответа с учетом ключевых слов    
        elif check_message_for_keywords(message.text):
            response = choice(responses)
            await message.reply(response)
        # Проверка для ответа фото с учетом ключевых слов    
        elif check_message_for_keywords_photo(message.text):
            photo_path = send_random_photo()
            if photo_path:
                await client.send_photo(chat_id=message.chat.id, photo=photo_path, reply_to_message_id=message.message_id)
            else:
                await message.reply("Фото отсутствуют.")
        elif message.reply_to_message and message.reply_to_message.from_user.id == client.me.id:
            # Если сообщение является ответом на сообщение бота
            response = choice(responses)
            await message.reply(response)

# Запуск бота
app.run()