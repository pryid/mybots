# Стандартные библиотеки Python
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Внешние библиотеки
from pyrogram import Client, filters
from pyrogram.types import Message, InlineQueryResultArticle, InputTextMessageContent

# Локальные импорты
import constants

# Функция для чтения и парсинга файла с правилами
def parse_rules():
    with open('filter.txt', 'r') as file:
        file_contents = file.read()

    pattern = r'\|\|([^\^]+)\^\$removeparam=([^\n]+)'
    rules = {}

    for domain, params in re.findall(pattern, file_contents):
        params = params.split('|')
        params = list(set([param.strip() for param in params if param.strip()]))

        if domain in rules:
            rules[domain].extend(params)
            rules[domain] = list(set(rules[domain]))
        else:
            rules[domain] = params

    return rules

rules = parse_rules()

# Функция для удаления параметров из URL
def remove_parameters_from_url(url, rules):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    domain = parsed_url.netloc

    if domain in rules:
        for param in rules[domain]:
            query_params.pop(param, None)

    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))

    return new_url

# Создание клиента Pyrogram
app = Client("sitrim", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
# Функция для логирования
def log_action(user, action):
    log_message = f"@{user.username or ''}, {user.first_name or ''} {user.last_name or ''}, ID: {user.id} - {action}"
    app.send_message(constants.LOG_CHANNEL_ID, log_message)

@app.on_message(filters.private & filters.command("start"))
def start(client, message: Message):
    message.reply_text("Hello. Send me a URL to clean it.")
    log_action(message.from_user, "Started the bot")

@app.on_message(filters.private & filters.regex(r'https?://[^\s]+'))
def clean_url(client, message: Message):
    url = message.text
    cleaned_url = remove_parameters_from_url(url, rules)
    message.reply_text(f"Cleaned URL:\n{cleaned_url}")
    log_action(message.from_user, f"Cleaned URL: {url} -> {cleaned_url}")

@app.on_inline_query()
def answer(client, inline_query):
    try:
        query = inline_query.query
        if query.startswith("http"):
            cleaned_url = remove_parameters_from_url(query, rules)
            inline_query.answer([InlineQueryResultArticle(
                title="Cleaned URL",
                input_message_content=InputTextMessageContent(cleaned_url)
            )])
            log_action(inline_query.from_user, f"Cleaned inline URL: {query} -> {cleaned_url}")
    except Exception as e:
        log_action(inline_query.from_user, f"Error in inline query: {e}")

app.run()
