"""Посещения: записи личной коллекции «пользователь был на мероприятии»."""

from datetime import date

from models.events import is_past_event
from models.ratings import format_score, get_rating
from utils import find_by, next_id


# Проверяет, есть ли уже это мероприятие в коллекции пользователя
def has_visit(visits: list[dict], user_id: int, event_id: int) -> bool:
    return any(
        visit["user_id"] == user_id and visit["event_id"] == event_id
        for visit in visits
    )


# Добавляет посещение, если мероприятие уже прошло и его нет в коллекции
def add_visit(visits: list[dict], user_id: int, event: dict,
              today: date) -> dict:
    if not is_past_event(event, today):
        raise ValueError("Мероприятие еще не прошло.")
    if has_visit(visits, user_id, event["id"]):
        raise ValueError("Мероприятие уже есть в коллекции.")
    visit = {"id": next_id(visits), "user_id": user_id,
             "event_id": event["id"]}
    visits.append(visit)
    return visit


# Возвращает посещения выбранного пользователя
def get_user_visits(visits: list[dict], user_id: int) -> list[dict]:
    return [visit for visit in visits if visit["user_id"] == user_id]


# Удаляет посещение по номеру, возвращает True, если оно было найдено
def remove_visit(visits: list[dict], visit_id: int) -> bool:
    visit = find_by(visits, "id", visit_id)
    if visit is None:
        return False
    visits.remove(visit)
    return True


# Выводит карточку посещения: мероприятие, дата, сколько дней прошло, оценка
def show_visit_card(visit: dict, events: list[dict], ratings: list[dict],
                    today: date) -> None:
    event = find_by(events, "id", visit["event_id"])
    if event is None:
        print(f"Посещение №{visit['id']}: мероприятие не найдено")
        return
    event_date = date.fromisoformat(event["date"])
    days_passed = (today - event_date).days
    when = "сегодня" if days_passed == 0 else f"{days_passed} дн. назад"
    score = get_rating(ratings, visit["id"])
    print(f"Посещение №{visit['id']}: {event['title']} ({event['category']})")
    print(f"Дата: {event_date.strftime('%d.%m.%Y')} ({when})")
    print(f"Оценка: {format_score(score)}")
