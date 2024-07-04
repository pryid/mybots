# Использование официального образа Python 3.12
FROM python:3.12

# Установка рабочей директории в контейнере
WORKDIR /app

# Клонирование репозитория
RUN git clone https://github.com/pryid/mybots.git .

# Установка зависимостей из файла requirements.txt
RUN pip install -r requirements.txt

# Установка переменных окружения
ENV TGAPI_ID=[telegram api id] \
    TGAPI_HASH=[telegram api hash] \
    TGAPI_ADMIN=[bot owner id] \
    LOG_CHANNEL_ID=[channel for logging] \
    SBERPRIMEPLUS_TOKEN=[bot token] \
    TTS_CHECKER_TOKEN=[bot token] \
    SITRIM_TOKEN=[bot token] \
    MUSARSKOY_TOKEN=[bot token] \
    MUSAR_CHANNEL_ID=[channel for musarskoy documents]
# Команда для запуска ботов
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]
