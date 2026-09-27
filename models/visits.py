"""Посещения: класс Visit и функции работы с коллекцией посещений."""

from datetime import date

from utils import next_id

from .events import Event, find_event_by_id
from .ratings import Rating
from .users import User, find_user_by_id


# Посещение: связывает пользователя с мероприятием и хранит его оценку
class Visit:
    # Создает посещение и запоминает объекты пользователя и мероприятия
    def __init__(self, visit_id: int, user: User, event: Event,
                 rating: Rating | None = None) -> None:
        self.id = visit_id
        self.user = user
        self.event = event
        self.rating = rating

    # Ставит оценку посещению: новая оценка или замена старой
    def rate(self, score_text: str, rating_id: int) -> Rating:
        score = Rating.parse_score(score_text)
        if self.rating is not None:
            rating_id = self.rating.id
        self.rating = Rating(rating_id, score)
        return self.rating

    # Считает, сколько дней прошло с даты мероприятия
    def days_passed(self, today: date) -> int:
        return (today - self.event.date).days

    # Формирует карточку посещения для просмотра в коллекции
    def card(self, today: date) -> str:
        days = self.days_passed(today)
        when = "сегодня" if days == 0 else f"{days} дн. назад"
        score = "не выставлена" if self.rating is None else str(self.rating)
        return (f"{self}\n"
                f"Дата: {self.event.date.strftime('%d.%m.%Y')} ({when})\n"
                f"Оценка: {score}")

    # Создает посещение из данных JSON, находя пользователя и мероприятие
    @classmethod
    def from_data(cls, data: dict, users: list[User],
                  events: list[Event]) -> "Visit | None":
        user = find_user_by_id(users, data["user_id"])
        event = find_event_by_id(events, data["event_id"])
        if user is None or event is None:
            return None
        return cls(data["id"], user, event)

    # Превращает посещение в данные для JSON (связи — по номерам)
    def to_data(self) -> dict:
        return {"id": self.id, "user_id": self.user.id,
                "event_id": self.event.id}

    # Строковое представление посещения
    def __str__(self) -> str:
        return (f"Посещение №{self.id}: {self.event.title} "
                f"({self.event.category})")


# Ищет посещение по номеру; если его нет — возвращает None
def find_visit_by_id(visits: list[Visit], visit_id: int) -> Visit | None:
    for visit in visits:
        if visit.id == visit_id:
            return visit
    return None


# Проверяет, есть ли уже это мероприятие в коллекции пользователя
def has_visit(visits: list[Visit], user: User, event: Event) -> bool:
    return any(visit.user.id == user.id and visit.event.id == event.id
               for visit in visits)


# Создает объект Visit, если мероприятие прошло и его нет в коллекции
def add_visit(visits: list[Visit], user: User, event: Event,
              today: date) -> Visit:
    if not event.is_past(today):
        raise ValueError("Мероприятие еще не прошло.")
    if has_visit(visits, user, event):
        raise ValueError("Мероприятие уже есть в коллекции.")
    visit = Visit(next_id(visits), user, event)
    visits.append(visit)
    return visit


# Возвращает посещения выбранного пользователя
def get_user_visits(visits: list[Visit], user: User) -> list[Visit]:
    return [visit for visit in visits if visit.user.id == user.id]


# Удаляет посещение по номеру вместе с его оценкой
def remove_visit(visits: list[Visit], visit_id: int) -> bool:
    visit = find_visit_by_id(visits, visit_id)
    if visit is None:
        return False
    visits.remove(visit)
    return True


# Собирает оценки всех посещений в один список
def collect_ratings(visits: list[Visit]) -> list[Rating]:
    return [visit.rating for visit in visits if visit.rating is not None]
