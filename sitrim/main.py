import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineQueryResultArticle, InputTextMessageContent
from url_cleaner import UrlCleaner
from constants import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID

# Настройка уровня логирования для Pyrogram
logging.getLogger('pyrogram').setLevel(logging.WARNING)

# Асинхронная функция для обновления правил
async def update_rules_periodically():
    while True:
        try:
            UrlCleaner().ruler.update_rules()
        except Exception as e:
            await log_error(f"Error updating rules: {e}")
        await asyncio.sleep(36000)  # Спать 36000 секунд (10 часов)

# Функция для удаления параметров из URL
def remove_parameters_from_url(url):
    try:
        return UrlCleaner().clean(url)
    except Exception as e:
        asyncio.create_task(log_error(f"Error cleaning URL: {e}"))
        return url

# Создание клиента Pyrogram
app = Client("sitrim", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Асинхронная функция для логирования
async def log_action(user, action):
    log_message = f"@{user.username or ''}, {user.first_name or ''} {user.last_name or ''}, ID: {user.id} - {action}"
    try:
        await app.send_message(LOG_CHANNEL_ID, log_message)
    except Exception as e:
        await log_error(f"Error logging action: {e}")

async def log_error(error_message):
    try:
        await app.send_message(LOG_CHANNEL_ID, error_message)
    except Exception as e:
        # В случае ошибки логирования в канал, ничего не делаем
        pass

@app.on_message(filters.private & filters.command("start"))
async def start(client, message: Message):
    await message.reply_text("Hello. Send me a URL to clean it.")
    await log_action(message.from_user, "Started the bot")

@app.on_message(filters.private & filters.regex(r'https?://[^\s]+'))
async def clean_url(client, message: Message):
    url = message.text
    cleaned_url = remove_parameters_from_url(url)
    await message.reply_text(f"Cleaned URL:\n{cleaned_url}")
    await log_action(message.from_user, f"Cleaned URL: {url} -> {cleaned_url}")

@app.on_inline_query()
async def answer(client, inline_query):
    try:
        query = inline_query.query
        if query.startswith("http"):
            cleaned_url = remove_parameters_from_url(query)
            await inline_query.answer([InlineQueryResultArticle(
                title="Cleaned URL",
                input_message_content=InputTextMessageContent(cleaned_url)
            )])
            await log_action(inline_query.from_user, f"Cleaned inline URL: {query} -> {cleaned_url}")
    except Exception as e:
        await log_error(f"Error in inline query: {e}")

# Запуск бота
if __name__ == "__main__":
    try:
        asyncio.create_task(update_rules_periodically())  # Запуск периодической задачи
        app.run()
    except Exception as e:
        print(f"Error starting bot: {e}")