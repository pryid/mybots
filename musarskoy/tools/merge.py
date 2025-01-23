import json

# Функция для чтения и очистки данных из JSON файла
def read_and_clean_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        # Удаление пустых строк
        clean_data = [item for item in data['responses'] if item.strip()]
    return clean_data

# Функция для последовательного объединения и удаления дубликатов
def sequential_merge(orig_file, output_file, result_file):
    orig_data = read_and_clean_json(orig_file)
    output_data = read_and_clean_json(output_file)

    # Создание списка для сохранения уникальных значений
    merged_data = []

    # Добавление элементов из файла orig.json
    for item in orig_data:
        if item not in merged_data:
            merged_data.append(item)

    # Добавление элементов из файла output.json
    for item in output_data:
        if item not in merged_data:
            merged_data.append(item)

    # Сохранение в новый файл
    with open(result_file, 'w', encoding='utf-8') as file:
        json.dump({'responses': merged_data}, file, ensure_ascii=False, indent=4)

# Пути к файлам
orig_file_path = 'orig.json'
output_file_path = 'output.json'
result_file_path = 'responses.json'

# Вызов функции для объединения и сохранения данных
sequential_merge(orig_file_path, output_file_path, result_file_path)
