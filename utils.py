"""Вспомогательные функции: id, поиск записей и безопасный ввод."""

from datetime import date, datetime


# Возвращает следующий свободный идентификатор для списка записей
def next_id(items: list[dict]) -> int:
    return max((item["id"] for item in items), default=0) + 1


# Ищет запись, у которой поле field равно value; если нет — возвращает None
def find_by(items: list[dict], field: str, value: object) -> dict | None:
    for item in items:
        if item[field] == value:
            return item
    return None


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
