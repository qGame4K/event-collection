"""Вспомогательные функции: номера объектов и безопасный ввод."""

from datetime import date, datetime


# Возвращает следующий свободный номер для коллекции объектов
def next_id(items: list) -> int:
    return max((item.id for item in items), default=0) + 1


# Запрашивает целое число, пока пользователь не введет его правильно
def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Нужно ввести целое число.")


# Запрашивает дату в формате ДД.ММ.ГГГГ, пока ввод не станет корректным
def input_date(prompt: str) -> date:
    while True:
        text = input(prompt).strip()
        try:
            return datetime.strptime(text, "%d.%m.%Y").date()
        except ValueError:
            print("Нужна дата в формате ДД.ММ.ГГГГ.")
