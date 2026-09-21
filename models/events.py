"""Мероприятия: события, которые пользователь может посетить."""

from datetime import date

from utils import next_id


# Добавляет мероприятие после проверки названия
def add_event(events: list[dict], title: str, category: str,
              event_date: date) -> dict:
    title = title.strip()
    if not title:
        raise ValueError("Название не может быть пустым.")
    event = {
        "id": next_id(events),
        "title": title,
        "category": category.strip().lower() or "другое",
        "date": event_date.isoformat(),
    }
    events.append(event)
    return event


# Проверяет, что мероприятие уже состоялось (дата не позже сегодняшней)
def is_past_event(event: dict, today: date) -> bool:
    return date.fromisoformat(event["date"]) <= today


# Ищет мероприятия по части названия (пустой запрос — все мероприятия)
def find_events(events: list[dict], query: str) -> list[dict]:
    query = query.strip().lower()
    return [event for event in events if query in event["title"].lower()]


# Возвращает мероприятия, отсортированные по дате
def sort_events_by_date(events: list[dict]) -> list[dict]:
    return sorted(events, key=lambda event: event["date"])


# Возвращает множество категорий мероприятий без повторов
def get_categories(events: list[dict]) -> set[str]:
    return {event["category"] for event in events}


# Формирует строку с данными мероприятия для вывода
def format_event(event: dict) -> str:
    event_date = date.fromisoformat(event["date"]).strftime("%d.%m.%Y")
    title = f"{event['title']} ({event['category']})"
    return f"{event['id']}. {event_date} {title}"
