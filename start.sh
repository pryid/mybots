#!/bin/bash

# Предполагая, что start.sh запускается из корневой директории проекта

# Запуск первого скрипта
cd tts_checker
python main.py &
cd ..

# Запуск второго скрипта
cd sberprimeplus
python main.py &
cd ..

# Запуск третьего скрипта
cd sitrim
python main.py &
cd ..

# Запуск четвертого скрипта
cd musarskoy
python main.py &
cd ..

# Ожидание завершения всех скриптов
wait
