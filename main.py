"""Event Collection — сервис личной коллекции посещенных мероприятий.

Начальный сценарий (ПР1): пользователь добавляет посещенное мероприятие
в личную коллекцию, ставит ему оценку и просматривает карточку посещения.
"""

from datetime import date

MIN_RATING = 1
MAX_RATING = 5


def add_visit(event_title, visit_date, today):
    """Проверяет, можно ли добавить посещение в личную коллекцию.

    Добавить можно мероприятие с заполненным названием,
    которое уже состоялось: дата посещения не позже сегодняшней.
    """
    has_title = event_title.strip() != ""
    is_past_event = visit_date <= today
    return has_title and is_past_event


def rate_event(rating_text):
    """Преобразует введенную оценку в целое число от 1 до 5.

    Возвращает 0, если введено не целое число или оно вне шкалы.
    """
    rating_text = rating_text.strip()
    if not rating_text.isdecimal():
        return 0

    rating = int(rating_text)
    if MIN_RATING <= rating <= MAX_RATING:
        return rating
    return 0


def get_visit_card(event_title, category, visit_date, rating, today):
    """Формирует текст карточки посещения для просмотра в коллекции."""
    days_passed = (today - visit_date).days
    if days_passed == 0:
        when = "сегодня"
    else:
        when = f"{days_passed} дн. назад"

    if rating == 0:
        rating_line = "не выставлена"
    else:
        stars = "★" * rating + "☆" * (MAX_RATING - rating)
        if rating >= 4:
            verdict = "понравилось"
        elif rating == 3:
            verdict = "нормально"
        else:
            verdict = "не понравилось"
        rating_line = f"{stars} {rating}/{MAX_RATING} — {verdict}"

    return (
        f"Мероприятие: {event_title} ({category})\n"
        f"Дата посещения: {visit_date.strftime('%d.%m.%Y')} ({when})\n"
        f"Оценка: {rating_line}"
    )


if __name__ == "__main__":
    today = date.today()

    # Пользователь и его коллекция
    user_name = "Иван"
    visits_count = 12

    # Мероприятие, которое посетил пользователь
    event_title = "Фестиваль уличной еды"
    event_category = "фестиваль"
    visit_date = date.fromisoformat("2026-09-05")

    print(f"Пользователь: {user_name}")
    print(f"Посещений в коллекции: {visits_count}")
    print()

    if add_visit(event_title, visit_date, today):
        visits_count += 1
        print(f"Мероприятие «{event_title}» добавлено в коллекцию.")
        print(f"Посещений в коллекции: {visits_count}")

        rating = rate_event(input("Оцените мероприятие от 1 до 5: "))
        if rating == 0:
            print("Оценка не распознана, посещение сохранено без оценки.")

        print()
        print(get_visit_card(event_title, event_category, visit_date,
                             rating, today))
    else:
        print(f"Нельзя добавить «{event_title}»: мероприятие еще не прошло.")
