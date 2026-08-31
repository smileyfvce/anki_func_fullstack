import random
import sys
import time
from typing import Dict, Tuple

STOP_WORD = "СТОП"
FILENAME = "words.txt"


def load_words(filename: str) -> Dict[str, str]:
    """
    Открывает файл со словами
    и формирует его в словарь
    """
    dictionary = {}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for row in file:
                line = row.strip()

                if not line:
                    continue

                if "," not in line:
                    continue

                parts = line.split(",", 1)

                if len(parts) != 2:
                    continue

                word = parts[0].strip()
                translation = parts[1].strip()

                if not word or not translation:
                    continue

                dictionary[word] = translation

        return dictionary

    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        sys.exit(1)


def print_statistics(score: int, total_time: float) -> None:
    """
    Выводит статистику игры:
    колличество правильных ответов и время
    """
    print(f"Ваш итоговый счёт: {score}")
    time_str = f"{total_time:.2f}"
    if score > 0:
        avg_time = total_time / score
        avg_str = f"{avg_time:.2f}"
        print(f"Время игры: {time_str} "
              f"секунд (среднее время: {avg_str} сек.)")
    else:
        print(f"Время игры: {time_str} секунд (среднее время: —)")


def ask_and_check(word: str, correct: str) -> Tuple[bool, bool, float]:
    """
    Запрашивает перевод слова,
    засекает время ответа
    """
    print(f"Ваше слово: {word}")
    start_time = time.time()
    translation_input = input("Ваш перевод: ").strip()
    end_time = time.time() - start_time

    if translation_input.upper() == STOP_WORD:
        return True, False, 0.0

    correct_word = translation_input.lower() == correct.lower()
    return False, correct_word, end_time


def start_game(words: Dict[str, str]) -> None:
    """
    Режим игры: игра выводит слово и просит перевод,
    выход осуществляется через стоп-слово
    """
    if not words:
        print("Словарь пуст. Сначала добавьте слова (пункт 2).")
        return
    print(f"Чтобы закончить, введите {STOP_WORD}")
    score = 0
    total_time = 0.0

    while True:
        word, correct = random.choice(list(words.items()))
        exit, correct_word, answer_time = ask_and_check(word, correct)

        if exit:
            print("Спасибо за игру!")
            break
        total_time += answer_time

        if correct_word:
            score += 1
            print(f"Верно! Время на ответ: {round(answer_time, 2)} секунд")
        else:
            print(
                f"Неправильно, правильный ответ: {correct}"
                f"(Время на ответ: {round(answer_time, 2)} секунд)"
            )
    print_statistics(score, total_time)


def train_until_mistake(words: Dict[str, str]) -> None:
    """
    Режим игры: игра выводит слово и просит перевод,
    игра продолжается до первой ошибки,
    выход осуществляется через стоп-слово
    """
    if not words:
        print("Словарь пуст. Сначала добавьте слова (пункт 2).")
        return
    print("Режим: игра до первой ошибки! Чтобы выйти вручную, введите СТОП")
    score = 0
    total_time = 0.0

    while True:
        word, correct = random.choice(list(words.items()))
        exit, correct_word, answer_time = ask_and_check(word, correct)

        if exit:
            print("Спасибо за игру!")
            break
        total_time += answer_time

        if correct_word:
            score += 1
            print(f"Верно! Всего очков: {score}"
                  f"(ответ за {answer_time:.2f} секунд)")
        else:
            print(f"Ошибка! Неверно. Правильный ответ: {correct}")
            break
    print_statistics(score, total_time)


def add_words(words: Dict[str, str]) -> None:
    """
    Добавляет новые пары ключ : значение
    """
    while True:

        word_input = input("Введите слово:").strip()

        if word_input.upper() == STOP_WORD:
            break
        if not word_input:
            print("Поле не может быть пустым")
            continue

        translation_input = input("Введите перевод:").strip()

        if translation_input.upper() == STOP_WORD:
            break
        if not translation_input:
            print("Поле не может быть пустым")
            continue
        words[word_input] = translation_input


def show_all_words(words: dict) -> None:
    """
    Показывает все пары ключ : значение
    находящиеся в словаре
    """
    if not words:
        print()
        return

    parts = [f"{word} - {translation}" for word, translation in words.items()]
    print("; ".join(parts))


def save_words(words: Dict[str, str], filename: str) -> None:
    """
    Сохраняет добавленые слова в файл words.txt
    """
    count = len(words)
    with open(filename, "w", encoding="utf-8") as file:
        for word, translation in words.items():
            file.write(f"{word},{translation}\n")
    print(f"Было сохранено {count} слов в файл {filename}")


def get_words_count(count: int) -> int:
    """
    Формирует правильный вывод текста
    """
    if 11 <= count % 100 <= 19:
        return "слов"
    elif count % 10 == 1:
        return "слово"
    elif 2 <= count % 10 <= 4:
        return "слова"
    else:
        return "слов"


def main() -> None:
    """
    Выводит меню приложения
    """
    words_dict = load_words(FILENAME)
    count = len(words_dict)
    format_text = get_words_count(count)
    print(f"Было загружено {count} {format_text} из файла {FILENAME}")
    while True:
        menu = """Меню:
        1. Начать игру
        2. Добавить слова
        3. Тренировка до первой ошибки
        4. Вывод всех слов
        5. Выход
        """
        print(menu)
        menu_choice = input("Пункт меню: ")

        if menu_choice == "1":
            start_game(words_dict)
        elif menu_choice == "2":
            add_words(words_dict)
        elif menu_choice == "3":
            train_until_mistake(words_dict)
        elif menu_choice == "4":
            show_all_words(words_dict)
        elif menu_choice == "5":
            save_words(words_dict, FILENAME)
            break


if __name__ == "__main__":
    main()
