"""Перенос данных проекта из JSON-файлов в базу данных SQLite."""

import json
import sqlite3
from pathlib import Path

from db.database import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"


# Читает JSON-файл проекта и возвращает список записей
def load_json(name: str) -> list[dict]:
    with open(DATA_DIR / name, encoding="utf-8") as file:
        return json.load(file)


# Создает таблицы по командам из файла sql/schema.sql
def create_schema(conn: sqlite3.Connection) -> None:
    with open(SCHEMA_FILE, encoding="utf-8") as file:
        conn.executescript(file.read())


# Очищает таблицы, чтобы импорт можно было выполнять повторно
def clear_tables(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM ratings")
    conn.execute("DELETE FROM visits")
    conn.execute("DELETE FROM events")
    conn.execute("DELETE FROM users")


# Переносит пользователей из users.json
def import_users(conn: sqlite3.Connection) -> int:
    users = load_json("users.json")
    conn.executemany(
        "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
        [(user["id"], user["name"], user["email"]) for user in users],
    )
    return len(users)


# Переносит мероприятия из events.json
def import_events(conn: sqlite3.Connection) -> int:
    events = load_json("events.json")
    conn.executemany(
        """
        INSERT INTO events (id, title, title_lower, category, date)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                event["id"],
                event["title"],
                event["title"].lower(),
                event["category"],
                event["date"],
            )
            for event in events
        ],
    )
    return len(events)


# Переносит посещения из visits.json
def import_visits(conn: sqlite3.Connection) -> int:
    visits = load_json("visits.json")
    conn.executemany(
        """
        INSERT INTO visits (id, user_id, event_id)
        VALUES (?, ?, ?)
        """,
        [
            (visit["id"], visit["user_id"], visit["event_id"])
            for visit in visits
        ],
    )
    return len(visits)


# Переносит оценки из ratings.json
def import_ratings(conn: sqlite3.Connection) -> int:
    ratings = load_json("ratings.json")
    conn.executemany(
        """
        INSERT INTO ratings (id, visit_id, score)
        VALUES (?, ?, ?)
        """,
        [
            (rating["id"], rating["visit_id"], rating["score"])
            for rating in ratings
        ],
    )
    return len(ratings)


# Создает схему и переносит данные всех четырех сущностей
def main() -> None:
    conn = get_connection()
    try:
        create_schema(conn)
        clear_tables(conn)
        users = import_users(conn)
        events = import_events(conn)
        visits = import_visits(conn)
        ratings = import_ratings(conn)
        conn.commit()
        print(f"Пользователей: {users}")
        print(f"Мероприятий: {events}")
        print(f"Посещений: {visits}")
        print(f"Оценок: {ratings}")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
