# Стандартные библиотеки Python
import json
from random import choice, randint

# Внешние библиотеки
from pyrogram import Client, filters

# Локальные импорты
from constants import API_ID, API_HASH, BOT_TOKEN

# Путь к файлу с ответами

responses_file = '/app/data/musarskoy_responses.json'

# Загрузка JSON-файла с ответами
with open(responses_file, "r") as file:
    data = json.load(file)
    responses = data["responses"]

# Функция для обновления и перезагрузки ответов
def update_and_reload_responses(new_response):
    responses.append(new_response)
    with open(responses_file, "w") as file:
        json.dump({"responses": responses}, file, ensure_ascii=False, indent=4)

# Создание клиента Pyrogram
app = Client("musarskoy", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Функция для проверки наличия ключевых слов в сообщении
def check_message_for_keywords(message_text):
    keywords = ["мусарской", "мусар", "мусор", "министр", "смешной"]
    message_text = message_text.lower()  # Приводим текст сообщения к нижнему регистру
    for keyword in keywords:
        if keyword in message_text:
            return True
    return False

# Обработчик сообщений
@app.on_message(filters.text)
async def echo(client, message):
    # Проверка ID пользователя
    if message.from_user.id == 1473899765:
    #if message.from_user.id == 152204223:
        update_and_reload_responses(message.text)
        #await message.reply("Ваше сообщение добавлено в список ответов.")
    else:
        # Генерация случайного числа от 1 до 100
        random_number = randint(1, 100)

        # Проверка случайного числа для ответа без учета ключевых слов
        if random_number == 1:
            response = choice(responses)
            await message.reply(response)
        elif check_message_for_keywords(message.text):
            response = choice(responses)
            await message.reply(response)
        elif message.reply_to_message and message.reply_to_message.from_user.id == client.me.id:
            # Если сообщение является ответом на сообщение бота
            response = choice(responses)
            await message.reply(response)

# Запуск бота
app.run()
