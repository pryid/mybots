import json

# Открываем файл JSON для чтения
with open('result.json', 'r', encoding='utf-8', errors='ignore') as file:
    data = json.load(file)

# Фильтруем массив "messages" и собираем текстовые элементы "text"
filtered_messages = [message["text"] for message in data["messages"] if message.get("from_id") == "user1473899765"]

# Объединяем текстовые элементы в один большой массив "responses"
responses = []
for text in filtered_messages:
    if isinstance(text, str):
        responses.append(text)
    elif isinstance(text, list):
        responses.extend(item["text"] for item in text if "text" in item)

# Создаем новый JSON объект с массивом "responses"
result = {"responses": responses}

# Записываем результат в новый файл JSON
with open('output.json', 'w', encoding='utf-8') as output_file:
    json.dump(result, output_file, ensure_ascii=False, indent=2)

print("Готово! Результат сохранен в output.json")
