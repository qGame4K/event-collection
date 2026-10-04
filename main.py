"""Event Collection — консольное приложение личной коллекции мероприятий."""

from datetime import date

from models import Event, User, Visit
from models.events import (add_event, find_event_by_id, find_events,
                           get_categories, sort_events_by_date)
from models.ratings import average_score
from models.users import add_user, find_user_by_id, find_users, sort_users
from models.visits import (add_visit, collect_ratings, find_visit_by_id,
                           get_user_visits, remove_visit)
from storage import (EVENTS_FILE, RATINGS_FILE, USERS_FILE, VISITS_FILE,
                     load_events, load_ratings, load_users, load_visits,
                     save_events, save_ratings, save_users, save_visits)
from utils import input_date, input_int, next_id

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


# Сценарий «отметить посещение»: находит объекты и создает посещение
def add_new_visit(visits: list[Visit], users: list[User],
                  events: list[Event], today: date) -> None:
    user = find_user_by_id(users, input_int("ID пользователя: "))
    event = find_event_by_id(events, input_int("ID мероприятия: "))
    if user is None:
        raise ValueError("Пользователь не найден.")
    if event is None:
        raise ValueError("Мероприятие не найдено.")
    visit = add_visit(visits, user, event, today)
    save_visits(VISITS_FILE, visits)
    print(f"{visit} — добавлено в коллекцию.")


# Точка запуска: создает объекты из JSON и обрабатывает пункты меню
def main() -> None:
    users = load_users(USERS_FILE)
    events = load_events(EVENTS_FILE)
    visits = load_visits(VISITS_FILE, users, events)
    load_ratings(RATINGS_FILE, visits)
    today = date.today()

    while True:
        print("\n=== Event Collection ===")
        print("\n".join(MENU))
        try:
            choice = input("Выберите действие: ").strip()
            if choice == "1":
                query = input("Часть имени (Enter — все): ")
                for user in sort_users(find_users(users, query)):
                    print(user)
            elif choice == "2":
                name = input("Имя: ")
                email = input("Email: ")
                user = add_user(users, name, email)
                save_users(USERS_FILE, users)
                print(f"Добавлен пользователь {user}")
            elif choice == "3":
                query = input("Часть названия (Enter — все): ")
                for event in sort_events_by_date(find_events(events, query)):
                    print(event)
            elif choice == "4":
                title = input("Название: ")
                category = input("Категория: ")
                event_date = input_date("Дата (ДД.ММ.ГГГГ): ")
                event = add_event(events, title, category, event_date)
                save_events(EVENTS_FILE, events)
                print(f"Добавлено мероприятие {event}")
            elif choice == "5":
                add_new_visit(visits, users, events, today)
            elif choice == "6":
                visit_id = input_int("Номер посещения: ")
                visit = find_visit_by_id(visits, visit_id)
                if visit is None:
                    raise ValueError("Посещение не найдено.")
                score_text = input("Оценка от 1 до 5: ")
                visit.rate(score_text, next_id(collect_ratings(visits)))
                save_ratings(RATINGS_FILE, visits)
                print(f"Оценка сохранена: {visit.rating}")
            elif choice == "7":
                visit_id = input_int("Номер посещения: ")
                if not remove_visit(visits, visit_id):
                    raise ValueError("Посещение не найдено.")
                save_visits(VISITS_FILE, visits)
                save_ratings(RATINGS_FILE, visits)
                print("Посещение удалено.")
            elif choice == "8":
                user = find_user_by_id(users, input_int("ID пользователя: "))
                if user is None:
                    raise ValueError("Пользователь не найден.")
                user_visits = get_user_visits(visits, user)
                print(f"Коллекция пользователя {user.name}")
                print(f"Посещений: {len(user_visits)}")
                for visit in user_visits:
                    print()
                    print(visit.card(today))
            elif choice == "9":
                ratings = collect_ratings(visits)
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
