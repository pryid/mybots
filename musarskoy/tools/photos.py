import json

# Путь к исходному файлу
input_file = 'filelist.txt'

# Путь к файлу, который будет создан
output_file = 'photos.json'

# Чтение файла и преобразование данных
photo_ids = []
with open(input_file, 'r') as file:
    for line in file:
        file_id = line.strip().replace('.jpg', '')  # Удаление пробелов и ".jpg"
        photo_ids.append(file_id)

# Создание JSON-структуры
data = {
    "photo_ids": photo_ids
}

# Сохранение данных в JSON-файл
with open(output_file, 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"JSON data has been written to {output_file}")
