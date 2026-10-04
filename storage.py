"""Хранение данных: JSON превращается в объекты и обратно."""

import json
from pathlib import Path

from models import Event, Rating, User, Visit
from models.visits import find_visit_by_id

DATA_DIR = Path(__file__).parent / "data"
USERS_FILE = DATA_DIR / "users.json"
EVENTS_FILE = DATA_DIR / "events.json"
VISITS_FILE = DATA_DIR / "visits.json"
RATINGS_FILE = DATA_DIR / "ratings.json"


# Загружает список записей из JSON; при ошибке файла возвращает пустой список
def load_json(path: Path) -> list[dict]:
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {path.name} не найден, список будет пустым.")
    except json.JSONDecodeError:
        print(f"Файл {path.name} поврежден, список будет пустым.")
    return []


# Сохраняет список записей в JSON-файл
def save_json(path: Path, items: list[dict]) -> None:
    try:
        path.parent.mkdir(exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False, indent=2)
            file.write("\n")
    except OSError:
        print(f"Не удалось сохранить файл {path.name}.")


# Загружает пользователей и превращает их в объекты User
def load_users(path: Path) -> list[User]:
    return [User.from_data(data) for data in load_json(path)]


# Сохраняет объекты User в JSON
def save_users(path: Path, users: list[User]) -> None:
    save_json(path, [user.to_data() for user in users])


# Загружает мероприятия и превращает их в объекты Event
def load_events(path: Path) -> list[Event]:
    return [Event.from_data(data) for data in load_json(path)]


# Сохраняет объекты Event в JSON
def save_events(path: Path, events: list[Event]) -> None:
    save_json(path, [event.to_data() for event in events])


# Загружает посещения и связывает их с объектами User и Event
def load_visits(path: Path, users: list[User],
                events: list[Event]) -> list[Visit]:
    visits = []
    for data in load_json(path):
        visit = Visit.from_data(data, users, events)
        if visit is not None:
            visits.append(visit)
    return visits


# Сохраняет объекты Visit в JSON (связи — по номерам)
def save_visits(path: Path, visits: list[Visit]) -> None:
    save_json(path, [visit.to_data() for visit in visits])


# Загружает оценки и раздает их посещениям
def load_ratings(path: Path, visits: list[Visit]) -> None:
    for data in load_json(path):
        visit = find_visit_by_id(visits, data["visit_id"])
        if visit is not None:
            visit.rating = Rating.from_data(data)


# Сохраняет оценки посещений в JSON
def save_ratings(path: Path, visits: list[Visit]) -> None:
    save_json(path, [visit.rating.to_data(visit.id)
                     for visit in visits if visit.rating is not None])
