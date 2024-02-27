# Использование официального образа Python 3.12
FROM python:3.12

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файла requirements.txt из локальной папки в контейнер
# Этот шаг необходим, если вы хотите установить зависимости при сборке образа,
# но может быть опущен, если вы устанавливаете зависимости непосредственно в монтируемой папке
COPY requirements.txt /app/

# Установка зависимостей из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Установка переменных окружения
ENV TGAPI_ID=[telegram api id] \
    TGAPI_HASH=[telegram api hash] \
    TGAPI_ADMIN=[bot owner id] \
    LOG_CHANNEL_ID=[channel for logging id] \
    SBERPRIMEPLUS_TOKEN=[bot token] \
    TTS_CHECKER_TOKEN=[bot token] \
    SITRIM_TOKEN=[bot token] \
    MUSARSKOY_TOKEN=[bot token]

# Установка прав на выполнение для start.sh
# Этот шаг предполагает, что скрипт start.sh находится в вашей локальной папке
RUN chmod +x /app/start.sh

# Команда для запуска ботов
CMD ["/app/start.sh"]