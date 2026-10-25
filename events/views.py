"""Страницы мероприятий: данные берутся из базы данных SQLite."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one

# Список мероприятий по дате
EVENTS_SQL = """
    SELECT
        id,
        title,
        category,
        strftime('%d.%m.%Y', date) AS date_display
    FROM events
    ORDER BY date
"""

# Карточка мероприятия: число посещений и средняя оценка
EVENT_SQL = """
    SELECT
        events.id,
        events.title,
        events.category,
        strftime('%d.%m.%Y', events.date) AS date_display,
        events.date <= date('now') AS is_past,
        COUNT(visits.id) AS visits_count,
        ROUND(AVG(ratings.score), 1) AS average_score
    FROM events
    LEFT JOIN visits
        ON visits.event_id = events.id
    LEFT JOIN ratings
        ON ratings.visit_id = visits.id
    WHERE events.id = ?
    GROUP BY events.id
"""

# Поиск по части названия; категория добавляется отдельным условием
SEARCH_SQL = """
    SELECT
        id,
        title,
        category,
        strftime('%d.%m.%Y', date) AS date_display
    FROM events
    WHERE title_lower LIKE ?
"""

# Категории без повторов для выпадающего списка формы
CATEGORIES_SQL = """
    SELECT DISTINCT category
    FROM events
    ORDER BY category
"""


# Страница /events/: список мероприятий из базы данных
def events(request: HttpRequest) -> HttpResponse:
    context = {
        "events": fetch_all(EVENTS_SQL),
    }
    return render(request, "events/event_list.html", context)


# Страница /events/search/: поиск мероприятий по названию и категории
def event_search(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    sql = SEARCH_SQL
    params = [f"%{query.lower()}%"]
    if category:
        sql += " AND category = ?"
        params.append(category)
    sql += " ORDER BY date"
    context = {
        "events": fetch_all(sql, tuple(params)),
        "categories": fetch_all(CATEGORIES_SQL),
        "query": query,
        "category": category,
    }
    return render(request, "events/event_search.html", context)


# Страница /events/<id>/: карточка мероприятия, иначе ответ 404
def event_detail(request: HttpRequest, event_id: int) -> HttpResponse:
    event = fetch_one(EVENT_SQL, (event_id,))
    context = {
        "event": event,
    }
    return render(request, "events/event_detail.html", context,
                  status=404 if event is None else 200)
