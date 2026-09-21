"""Event Collection — консольное приложение личной коллекции мероприятий."""

from datetime import date
from pathlib import Path

from events import (add_event, find_events, format_event, get_categories,
                    sort_events_by_date)
from ratings import average_score, rate_event, remove_rating
from storage import load_json, save_json
from users import add_user, find_users, format_user, sort_users
from utils import find_by, input_date, input_int
from visits import add_visit, get_user_visits, remove_visit, show_visit_card

DATA_DIR = Path(__file__).parent / "data"
USERS_FILE = DATA_DIR / "users.json"
EVENTS_FILE = DATA_DIR / "events.json"
VISITS_FILE = DATA_DIR / "visits.json"
RATINGS_FILE = DATA_DIR / "ratings.json"

MENU = (
    "1. Пользователи",
    "2. Добавить пользователя",
    "3. Мероприятия",
    "4. Добавить мероприятие",
    "5. Отметить посещение",
    "6. Оценить посещение",
    "7. Удалить посещение",
    "8. Коллекция пользователя",
    "9. Статистика",
    "0. Выход",
)


# Точка запуска: загружает данные из JSON и обрабатывает пункты меню
def main() -> None:
    users = load_json(USERS_FILE)
    events = load_json(EVENTS_FILE)
    visits = load_json(VISITS_FILE)
    ratings = load_json(RATINGS_FILE)
    today = date.today()

    while True:
        print("\n=== Event Collection ===")
        print("\n".join(MENU))
        try:
            choice = input("Выберите действие: ").strip()
            if choice == "1":
                query = input("Часть имени (Enter — все): ")
                for user in sort_users(find_users(users, query)):
                    print(format_user(user))
            elif choice == "2":
                name = input("Имя: ")
                email = input("Email: ")
                user = add_user(users, name, email)
                save_json(USERS_FILE, users)
                print(f"Добавлен пользователь {format_user(user)}")
            elif choice == "3":
                query = input("Часть названия (Enter — все): ")
                for event in sort_events_by_date(find_events(events, query)):
                    print(format_event(event))
            elif choice == "4":
                title = input("Название: ")
                category = input("Категория: ")
                event_date = input_date("Дата (ДД.ММ.ГГГГ): ")
                event = add_event(events, title, category, event_date)
                save_json(EVENTS_FILE, events)
                print(f"Добавлено мероприятие {format_event(event)}")
            elif choice == "5":
                user = find_by(users, "id", input_int("ID пользователя: "))
                event = find_by(events, "id", input_int("ID мероприятия: "))
                if user is None:
                    raise ValueError("Пользователь не найден.")
                if event is None:
                    raise ValueError("Мероприятие не найдено.")
                visit = add_visit(visits, user["id"], event, today)
                save_json(VISITS_FILE, visits)
                print(f"Посещение №{visit['id']} добавлено в коллекцию.")
            elif choice == "6":
                visit_id = input_int("Номер посещения: ")
                if find_by(visits, "id", visit_id) is None:
                    raise ValueError("Посещение не найдено.")
                score_text = input("Оценка от 1 до 5: ")
                rate_event(ratings, visit_id, score_text)
                save_json(RATINGS_FILE, ratings)
                print("Оценка сохранена.")
            elif choice == "7":
                visit_id = input_int("Номер посещения: ")
                if not remove_visit(visits, visit_id):
                    raise ValueError("Посещение не найдено.")
                remove_rating(ratings, visit_id)
                save_json(VISITS_FILE, visits)
                save_json(RATINGS_FILE, ratings)
                print("Посещение удалено.")
            elif choice == "8":
                user = find_by(users, "id", input_int("ID пользователя: "))
                if user is None:
                    raise ValueError("Пользователь не найден.")
                user_visits = get_user_visits(visits, user["id"])
                print(f"Коллекция пользователя {user['name']}")
                print(f"Посещений: {len(user_visits)}")
                for visit in user_visits:
                    print()
                    show_visit_card(visit, events, ratings, today)
            elif choice == "9":
                categories = ", ".join(sorted(get_categories(events)))
                print(f"Пользователей: {len(users)}")
                print(f"Мероприятий: {len(events)}")
                print(f"Посещений: {len(visits)}")
                print(f"Средняя оценка: {average_score(ratings)}")
                print(f"Категории: {categories}")
            elif choice == "0":
                break
            else:
                print("Нет такого пункта меню.")
        except ValueError as error:
            print(f"Ошибка: {error}")
        except (EOFError, KeyboardInterrupt):
            break
    print("До встречи!")


if __name__ == "__main__":
    main()
