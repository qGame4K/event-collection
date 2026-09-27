"""Пользователи: класс User и функции работы с коллекцией пользователей."""

from utils import next_id


# Пользователь сервиса: владелец личной коллекции мероприятий
class User:
    # Создает пользователя и сохраняет данные в атрибутах объекта
    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name
        self.email = email

    # Создает пользователя из данных JSON
    @classmethod
    def from_data(cls, data: dict) -> "User":
        return cls(data["id"], data["name"], data["email"])

    # Превращает пользователя в данные для JSON
    def to_data(self) -> dict:
        return {"id": self.id, "name": self.name, "email": self.email}

    # Строковое представление пользователя
    def __str__(self) -> str:
        return f"{self.id}. {self.name} <{self.email}>"


# Ищет пользователя по номеру; если его нет — возвращает None
def find_user_by_id(users: list[User], user_id: int) -> User | None:
    for user in users:
        if user.id == user_id:
            return user
    return None


# Проверяет, занят ли email другим пользователем (без учета регистра)
def is_email_taken(users: list[User], email: str) -> bool:
    emails = {user.email.lower() for user in users}
    return email.lower() in emails


# Создает объект User и добавляет его в коллекцию
def add_user(users: list[User], name: str, email: str) -> User:
    name = name.strip()
    email = email.strip()
    if not name:
        raise ValueError("Имя не может быть пустым.")
    if "@" not in email:
        raise ValueError("Некорректный email.")
    if is_email_taken(users, email):
        raise ValueError("Этот email уже занят.")
    user = User(next_id(users), name, email)
    users.append(user)
    return user


# Ищет пользователей по части имени (пустой запрос — все пользователи)
def find_users(users: list[User], query: str) -> list[User]:
    query = query.strip().lower()
    return [user for user in users if query in user.name.lower()]


# Возвращает пользователей, отсортированных по имени
def sort_users(users: list[User]) -> list[User]:
    return sorted(users, key=lambda user: user.name)
