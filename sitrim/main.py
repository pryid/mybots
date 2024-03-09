# Стандартные библиотеки Python
import re, asyncio

# Внешние библиотеки
from pyrogram import Client, filters
from pyrogram.types import Message, InlineQueryResultArticle, InputTextMessageContent
from url_cleaner import UrlCleaner

# Локальные импорты
from constants import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID

# Асинхронная функция для обновления правил
async def update_rules_periodically():
    while True:
        UrlCleaner().ruler.update_rules()
        await asyncio.sleep(3600)

# Функция для удаления параметров из URL
def remove_parameters_from_url(url):
    return UrlCleaner().clean(url)

# Создание клиента Pyrogram
app = Client("sitrim", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
# Функция для логирования
async def log_action(user, action):
    log_message = f"@{user.username or ''}, {user.first_name or ''} {user.last_name or ''}, ID: {user.id} - {action}"
    await app.send_message(LOG_CHANNEL_ID, log_message)

@app.on_message(filters.private & filters.command("start"))
async def start(client, message: Message):
    # Запуск асинхронной задачи обновления правил
    asyncio.create_task(update_rules_periodically())
    await message.reply_text("Hello. Send me a URL to clean it.")
    await log_action(message.from_user, "Started the bot")

@app.on_message(filters.private & filters.regex(r'https?://[^\s]+'))
def clean_url(client, message: Message):
    url = message.text
    cleaned_url = remove_parameters_from_url(url)
    message.reply_text(f"Cleaned URL:\n{cleaned_url}")
    log_action(message.from_user, f"Cleaned URL: {url} -> {cleaned_url}")

@app.on_inline_query()
def answer(client, inline_query):
    try:
        query = inline_query.query
        if query.startswith("http"):
            cleaned_url = remove_parameters_from_url(query)
            inline_query.answer([InlineQueryResultArticle(
                title="Cleaned URL",
                input_message_content=InputTextMessageContent(cleaned_url)
            )])
            log_action(inline_query.from_user, f"Cleaned inline URL: {query} -> {cleaned_url}")
    except Exception as e:
        log_action(inline_query.from_user, f"Error in inline query: {e}")

# Запуск бота
app.run()