# Стандартные библиотеки Python
import json
import re
import time
from datetime import timedelta

# Внешние библиотеки
import httpx
import psutil
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup

# Локальные импорты
from constants import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID, FEEDBACK_USER_ID

# Файл с данными

user_data_file = '/app/data/tts_checker.json'

app = Client("tts_checker", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

try:
    with open(user_data_file, 'r') as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}

waiting_for_card_number = {}
waiting_for_feedback = {}


def create_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("Баланс"), KeyboardButton("Номер карты"), KeyboardButton("Обратная связь")]
    ], resize_keyboard=True)


@app.on_message(filters.command(["start", "help"]))
async def start(client, message):
    await message.reply_text("Выберите одну из доступных команд.", reply_markup=create_keyboard())


@app.on_message(filters.command("status"))
async def status(client, message):
    if message.from_user.id == FEEDBACK_USER_ID:
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            ram_info = psutil.virtual_memory()
            uptime_seconds = int(time.time() - psutil.boot_time())
            uptime = str(timedelta(seconds=uptime_seconds))

            status_message = (
                f"🖥 CPU Load: {cpu_percent}%\n"
                f"🧠 RAM: {ram_info.used // (2 ** 20)} MiB / {ram_info.total // (2 ** 20)} MiB\n"
                f"⏱ Uptime: {uptime}"
            )
            await message.reply_text(status_message)
        except Exception as error:
            await message.reply_text(f"Ошибка при получении статуса: {error}")
    else:
        await message.reply_text("У вас нет доступа к этой команде.")


@app.on_message(filters.text & ~filters.regex("^/"))
async def on_text_message(client, message):
    user_id = message.from_user.id
    user_info = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}, @{message.from_user.username or ''} ({user_id})"
    await app.send_message(LOG_CHANNEL_ID, f"Received message from {user_info}: {message.text}")

    if message.text in ["Баланс", "Номер карты", "Обратная связь"]:
        waiting_for_card_number.pop(user_id, None)
        waiting_for_feedback.pop(user_id, None)

    if message.text == "Баланс":
        await check(client, message)
    elif message.text == "Номер карты":
        user_id_str = str(user_id)
        if user_id_str in user_data:
            await message.reply_text(f"Ваш текущий номер карты: {user_data[user_id_str]}\n"
                                     f"Если вы хотите изменить его, пожалуйста, введите новый номер карты.")
            waiting_for_card_number[user_id] = True
        else:
            waiting_for_card_number[user_id] = True
            await message.reply_text("Пожалуйста, отправьте номер карты.")
    elif message.text == "Обратная связь":
        waiting_for_feedback[user_id] = True
        await message.reply_text("Напишите ваши пожелания, претензии или предложения, если сообщение будет содержательным, я вам обязательно отвечу.")
    else:
        await handle_others(client, message, user_id)


async def handle_others(client, message, user_id):
    if user_id in waiting_for_card_number:
        await handle_card_number(client, message, user_id)
    elif user_id in waiting_for_feedback:
        await handle_feedback(client, message, user_id)
    else:
        await message.reply_text("Команда не распознана, нажмите /start.")


async def handle_card_number(client, message, user_id):
    card_number = message.text
    if not re.match(r"^\d{1,20}$", card_number):
        await message.reply_text("Пожалуйста, укажите корректный номер карты.")
        return
    user_data[str(user_id)] = card_number
    with open(user_data_file, 'w') as file:
        json.dump(user_data, file)
    del waiting_for_card_number[user_id]
    await message.reply_text(f"Ваш номер карты {card_number} был сохранён. Отправьте 'Баланс' для проверки баланса!")


async def handle_feedback(client, message, user_id):
    user_info = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}, @{message.from_user.username or ''}"
    feedback_text = f"Feedback from {user_info}:\n{message.text}"
    await app.send_message(FEEDBACK_USER_ID, feedback_text)
    del waiting_for_feedback[user_id]
    await message.reply_text("Ваше сообщение было отправлено. Спасибо за вашу обратную связь!")


@app.on_message(filters.command("check"))
async def check(client, message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        await message.reply_text("Пожалуйста, укажите номер карты, нажмите 'Номер карты'.")
        return

    card_number = user_data[user_id]
    url = 'https://oao-tts.ru/ttsfind/'
    data = {'submit': 'echo:card.check', 'nomer': card_number}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data)
            response.raise_for_status()
    except httpx.RequestError:
        await message.reply_text('Failed to send POST request.')
        return

    soup = BeautifulSoup(response.text, 'lxml')
    element = soup.select_one('.b-balance-card > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)')
    if element:
        for a_tag in element.find_all('a'):
            a_tag.decompose()
        await message.reply_text(element.text.strip())
    else:
        await message.reply_text('Скорее всего, вы ошиблись в номере карты, либо сейчас сервис недоступен. Нажмите \'Номер карты\' для повторного ввода номера карты.')


app.run()
