# Стандартные библиотеки Python
import datetime
import json
import re

# Внешние библиотеки
import psutil
from pyrogram import Client, filters, types

# Локальные импорты
from constants import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID


# Загрузка таблицы замен
with open('dictionary.json', 'r') as file:
    replacement_table = json.load(file)

# Функция для обработки текста
def process_text(text):
    words = re.findall(r'\b\w+\b|[.,!?;]', text)
    processed_text = []
    for word in words:
        if len(word) >= 3 and word[-1] in replacement_table:
            word = word[:-1] + replacement_table[word[-1]]
        processed_text.append(word)
    return ' '.join(processed_text)

# Создание экземпляра клиента
app = Client("sberprimeplus", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("Привет! Я бот, который может заменить последнюю букву каждого слова в вашем тексте!")
    user_info = f"{message.from_user.first_name} {message.from_user.last_name or ''}, @{message.from_user.username or ''}, ({message.from_user.id})"
    await client.send_message(LOG_CHANNEL_ID, f"Пользователь {user_info} начал чат.")

@app.on_message(filters.command("status"))
async def status(client, message):
    if message.from_user.id == 152204223:
        cpu_load = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
        cpu_temp = psutil.sensors_temperatures().get('coretemp', [None])[0]
        if cpu_temp: cpu_temp = cpu_temp.current
        else: cpu_temp = 'N/A'

        status_message = (
            f"🖥 CPU Load: {cpu_load}%\n"
            f"🧠 RAM: {ram.used / (1024 ** 2):.0f} MiB / {ram.total / (1024 ** 2):.0f} MiB\n"
            f"⏱ Uptime: {str(uptime).split('.')[0]}\n"
            f"🌡 CPU temp: {cpu_temp}° C"
        )
        await message.reply_text(status_message)

@app.on_message(filters.text & filters.private & ~filters.command(["start", "status"]))
async def echo(client, message):
    processed_text = process_text(message.text)
    await message.reply_text(processed_text)
    user_info = f"{message.from_user.first_name} {message.from_user.last_name or ''}, @{message.from_user.username or ''}, ({message.from_user.id})"
    await client.send_message(LOG_CHANNEL_ID, f"Пользователь {user_info} отправил сообщение: {message.text}\nОбработанный текст: {processed_text}")

@app.on_inline_query()
async def inline(client, query):
    query_text = query.query
    processed_text = process_text(query_text)

    # Создание InlineQueryResultArticle для отправки обратно пользователю
    results = [
        types.InlineQueryResultArticle(
            title="Обработанный Текст",
            input_message_content=types.InputTextMessageContent(processed_text),
            description=processed_text,
        )
    ]

    # Ответ пользователю с обработанным текстом
    await client.answer_inline_query(query.id, results=results, cache_time=10)
    user_info = f"{query.from_user.first_name} {query.from_user.last_name or ''}, @{query.from_user.username or ''}, ({query.from_user.id})"
    await client.send_message(LOG_CHANNEL_ID, f"Пользователь {user_info} сделал inline запрос: {query_text}\nОбработанный текст: {processed_text}")

# Запуск бота
app.run()
