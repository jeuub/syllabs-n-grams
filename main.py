import fasttext
from str_2_syllabs import get_comb
from process_text import process_text
import numpy as np

process_text()


def segment_words_into_syllables(text):
    words = text.split()
    segmented_text = []
    for word in words:
        syllables = get_comb(word)
        segmented_text.append(" ".join(syllables))
    return " ".join(segmented_text)


def get_combined_text():
    with open("combined_text.txt", "r", encoding="utf-8") as combined_file:
        text = combined_file.read()
        return text


text = get_combined_text()
segmented_text = segment_words_into_syllables(text)

with open("preprocessed_text.txt", "w") as f:
    f.write(segmented_text)

syllabs_model = fasttext.train_unsupervised("preprocessed_text.txt", model='skipgram')
fasttext_model = fasttext.train_supervised(input="combined_text.txt")


# Заменяем некорректные символы на пробел
def on_unicode_error(char):
    return ' '


seed_word = "кот"


def generate_text(model, seed_word, num_words=50):
    if isinstance(seed_word, str):
        seed_word = [seed_word]
    generated_text = " ".join(seed_word)
    for _ in range(num_words):
        nearest_word = model.get_nearest_neighbors(generated_text, k=1)[0][1]
        generated_text += " " + nearest_word
    return generated_text


# Результаты генерации текста
print("Обновленная модель", generate_text(syllabs_model, seed_word, 20))
print("обычная модель", generate_text(fasttext_model, seed_word, 20))


def text_similarity(model, text1, text2):
    # Получение векторного представления текстов с помощью обученной модели
    vector1 = model.get_sentence_vector(text1)
    vector2 = model.get_sentence_vector(text2)

    # Рассчитываем косинусное расстояние между векторами
    cosine_sim = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

    return cosine_sim


# Пример текстов для сравнения
text1 = "Это хороший день для прогулки в парке."
text2 = "Сегодня отличная погода для прогулки в парке."

print("Сходство текстов анализом обновленной модели:", text_similarity(syllabs_model, text1, text2))
print("Сходство текстов анализом обычной модели:", text_similarity(fasttext_model, text1, text2))


# Функция для поиска информации в тексте
def search_information(model, text, query, threshold=0.7):
    # Получаем векторное представление для запроса
    query_vector = model.get_sentence_vector(query)

    # Разбиваем текст на отдельные слова
    words = text.split()

    # Инициализируем список для хранения найденных слов
    found_words = []

    # Ищем слова в тексте, которые близки к запросу
    for word in words:
        word_vector = model.get_word_vector(word)
        cosine_sim = np.dot(query_vector, word_vector) / (np.linalg.norm(query_vector) * np.linalg.norm(word_vector))
        if cosine_sim >= threshold:
            found_words.append(word)

    return found_words


# Пример текста для поиска информации
text = "Машина – техническое устройство, предназначенное для перемещения грузов или людей."

# Запрос для поиска информации
query = "транспорт"

# Поиск информации в тексте на основе запроса
print("Найденные слова поиском обновленной модели:", search_information(syllabs_model, text, query))
print("Найденные слова поиском обычной модели:", search_information(fasttext_model, text, query))
