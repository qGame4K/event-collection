"""Загрузка и сохранение данных проекта в JSON-файлах."""

import json
from pathlib import Path


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
