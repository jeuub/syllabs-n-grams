import os

# Путь к папке с текстовыми файлами
folder_path = "texts"

# Список файлов в папке
files = os.listdir(folder_path)


# Считываем содержимое всех файлов и объединяем в одну строку
def process_text():
    all_text = ""
    for file_name in files:
        with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as file:
            text = file.read()
            all_text += text + "\n"

    # Пишем объединенный текст в файл
    with open("combined_text.txt", "w", encoding="utf-8") as combined_file:
        combined_file.write(all_text)