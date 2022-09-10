import random
import pickle
import argparse


def load_model():
    with open(args.model, 'rb') as f:
        return pickle.load(f)


def generation(args):
    dictionary = load_model()
    if args.prefix:
        next_word = args.prefix
        sequence = next_word
    else:
        sequence = next_word = random.choice(list(dictionary.keys()))
    for i in range(1, args.length):
        curr_word = random.choice(dictionary.setdefault(next_word))
        sequence += ' ' + curr_word
        next_word = curr_word
    return sequence


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', dest="model", default="model.pickle") #путь к обученной модели
    parser.add_argument('--prefix', dest="prefix", default=None) #префикс(начальное слово)
    parser.add_argument('--length', dest="length", type=int, default=10) #длина генерируемой последовательности
    args = parser.parse_args()
    print(generation(args))
