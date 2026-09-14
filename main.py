"""Event Collection — сервис личной коллекции посещенных мероприятий.

Начальный сценарий (ПР1): пользователь добавляет посещенное мероприятие
в личную коллекцию, ставит ему оценку и просматривает карточку посещения.
"""

from datetime import date

MIN_RATING = 1
MAX_RATING = 5


# Добавляет посещение в коллекцию, если есть название и мероприятие прошло
def add_visit(visits_count, event_title, visit_date, today):
    has_title = event_title.strip() != ""
    is_past_event = visit_date <= today
    if has_title and is_past_event:
        return visits_count + 1
    return visits_count


# Выставляет оценку мероприятию: проверяет ввод и возвращает число от 1 до 5
def rate_event(rating_text):
    rating_text = rating_text.strip()
    if not rating_text.isdecimal():
        return 0

    rating = int(rating_text)
    if MIN_RATING <= rating <= MAX_RATING:
        return rating
    return 0


# Выводит карточку посещения: мероприятие, дата, сколько дней прошло, оценка
def show_visit_card(event_title, category, visit_date, rating, today):
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

    print(f"Мероприятие: {event_title} ({category})")
    print(f"Дата посещения: {visit_date.strftime('%d.%m.%Y')} ({when})")
    print(f"Оценка: {rating_line}")


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

    new_visits_count = add_visit(visits_count, event_title, visit_date, today)

    if new_visits_count > visits_count:
        print(f"Мероприятие «{event_title}» добавлено в коллекцию.")
        print(f"Посещений в коллекции: {new_visits_count}")

        rating = rate_event(input("Оцените мероприятие от 1 до 5: "))
        if rating == 0:
            print("Оценка не распознана, посещение сохранено без оценки.")

        print()
        show_visit_card(event_title, event_category, visit_date,
                        rating, today)
    else:
        print("Посещение не добавлено: не указано название "
              "или мероприятие еще не прошло.")
