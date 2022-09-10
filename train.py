import re
import pickle
import argparse
import sys


def read_file(file_path):       # считываем файл как строку
    with open(file_path, 'r', encoding='utf8') as f:
        text = f.read()
    return text


def cleaning(text):
    # приводим текст к нижнему регистру
    text = text.lower()
    # создаем регулярное выражение для удаления лишних символов
    regular = r'[\d*…»«–\*+\#+\№\"\+\=+\?+\&\^\.+\;\,+\>+\(\)\/+\:\\+\[\]]'
    # удаляем лишние символы
    text = re.sub(regular, '', text)
    # удаляем лишние пробелы
    text = re.sub(r'[\-\s+]', ' ', text)
    text = re.sub(r'^\s+|\n|\r|\s+$', '', text)
    # возвращаем очищенные данные
    return text


def tokenization(text):      # == токенизируем очищенный текст ==
    return cleaning(text).split()


def n_grams(text):      # генериуем n-граммы и сохраняем их в словарь
    dictionary = {}
    for i in range(len(text) - 1):
        if dictionary.get(text[i], 0):
            pointer = dictionary.get(text[i])
            pointer.append(text[i + 1])
            dictionary[text[i]] = pointer
        else:
            dictionary[text[i]] = [text[i + 1]]
    return dictionary


def train(args):
    if args.input_dir:
        clear_data = tokenization(read_file(args.input_dir))
    else:
        clear_data = tokenization(sys.stdin.read())
    dictionary = n_grams(clear_data)
    with open(args.model, 'wb') as f:
        pickle.dump(dictionary, f)


if __name__ == "__main__":      # аргументы для запуска из консоли
    parser = argparse.ArgumentParser(description='Создание модели текста')
    parser.add_argument('--input_dir', dest="input_dir",
                        help='Путь к текстовому файлу для обучения')
    parser.add_argument('--model', dest="model", default="model.pickle",
                        help='Путь к файлу, в который сохраняется модель')
    args = parser.parse_args()
    train(args)
