"""Пользователи: владельцы личных коллекций мероприятий."""

from utils import next_id


# Проверяет, занят ли email другим пользователем (без учета регистра)
def is_email_taken(users: list[dict], email: str) -> bool:
    emails = {user["email"].lower() for user in users}
    return email.lower() in emails


# Добавляет пользователя после проверки имени и email
def add_user(users: list[dict], name: str, email: str) -> dict:
    name = name.strip()
    email = email.strip()
    if not name:
        raise ValueError("Имя не может быть пустым.")
    if "@" not in email:
        raise ValueError("Некорректный email.")
    if is_email_taken(users, email):
        raise ValueError("Этот email уже занят.")
    user = {"id": next_id(users), "name": name, "email": email}
    users.append(user)
    return user


# Ищет пользователей по части имени (пустой запрос — все пользователи)
def find_users(users: list[dict], query: str) -> list[dict]:
    query = query.strip().lower()
    return [user for user in users if query in user["name"].lower()]


# Возвращает пользователей, отсортированных по имени
def sort_users(users: list[dict]) -> list[dict]:
    return sorted(users, key=lambda user: user["name"])


# Формирует строку с данными пользователя для вывода
def format_user(user: dict) -> str:
    return f"{user['id']}. {user['name']} <{user['email']}>"
