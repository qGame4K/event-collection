"""Мероприятия: класс Event и функции работы с коллекцией мероприятий."""

from datetime import date

from utils import next_id


# Мероприятие: событие с названием, категорией и датой проведения
class Event:
    # Создает мероприятие и сохраняет данные в атрибутах объекта
    def __init__(self, event_id: int, title: str, category: str,
                 event_date: date) -> None:
        self.id = event_id
        self.title = title
        self.category = category
        self.date = event_date

    # Проверяет, что мероприятие уже состоялось
    def is_past(self, today: date) -> bool:
        return self.date <= today

    # Создает мероприятие из данных JSON
    @classmethod
    def from_data(cls, data: dict) -> "Event":
        return cls(data["id"], data["title"], data["category"],
                   date.fromisoformat(data["date"]))

    # Превращает мероприятие в данные для JSON
    def to_data(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "date": self.date.isoformat(),
        }

    # Строковое представление мероприятия
    def __str__(self) -> str:
        return (f"{self.id}. {self.date.strftime('%d.%m.%Y')} "
                f"{self.title} ({self.category})")


# Ищет мероприятие по номеру; если его нет — возвращает None
def find_event_by_id(events: list[Event], event_id: int) -> Event | None:
    for event in events:
        if event.id == event_id:
            return event
    return None


# Создает объект Event и добавляет его в коллекцию
def add_event(events: list[Event], title: str, category: str,
              event_date: date) -> Event:
    title = title.strip()
    if not title:
        raise ValueError("Название не может быть пустым.")
    category = category.strip().lower() or "другое"
    event = Event(next_id(events), title, category, event_date)
    events.append(event)
    return event


# Ищет мероприятия по части названия (пустой запрос — все мероприятия)
def find_events(events: list[Event], query: str) -> list[Event]:
    query = query.strip().lower()
    return [event for event in events if query in event.title.lower()]


# Возвращает мероприятия, отсортированные по дате
def sort_events_by_date(events: list[Event]) -> list[Event]:
    return sorted(events, key=lambda event: event.date)


# Возвращает множество категорий мероприятий без повторов
def get_categories(events: list[Event]) -> set[str]:
    return {event.category for event in events}
