"""Подключение к базе данных SQLite проекта."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "event_collection.sqlite"


# Открывает соединение: доступ к полям по именам и проверка внешних ключей
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Выполняет запрос с параметрами и возвращает все строки результата
def fetch_all(query: str, params: tuple = ()) -> list[sqlite3.Row]:
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchall()
    finally:
        conn.close()


# Выполняет запрос с параметрами и возвращает одну строку или None
def fetch_one(query: str, params: tuple = ()) -> sqlite3.Row | None:
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchone()
    finally:
        conn.close()
