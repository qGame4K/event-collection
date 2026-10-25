"""Страницы посещений и статистики: данные берутся из базы SQLite."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one

# Посещения с пользователем, мероприятием и оценкой
VISITS_SQL = """
    SELECT
        visits.id,
        users.name AS user_name,
        events.title AS event_title,
        strftime('%d.%m.%Y', events.date) AS date_display,
        ratings.score
    FROM visits
    JOIN users
        ON visits.user_id = users.id
    JOIN events
        ON visits.event_id = events.id
    LEFT JOIN ratings
        ON ratings.visit_id = visits.id
    ORDER BY events.date DESC
"""

# Карточка посещения по номеру
VISIT_SQL = """
    SELECT
        visits.id,
        users.name AS user_name,
        users.email AS user_email,
        events.id AS event_id,
        events.title AS event_title,
        events.category,
        strftime('%d.%m.%Y', events.date) AS date_display,
        ratings.score
    FROM visits
    JOIN users
        ON visits.user_id = users.id
    JOIN events
        ON visits.event_id = events.id
    LEFT JOIN ratings
        ON ratings.visit_id = visits.id
    WHERE visits.id = ?
"""

# Общие показатели проекта
TOTALS_SQL = """
    SELECT
        (SELECT COUNT(*) FROM users) AS users_count,
        (SELECT COUNT(*) FROM events) AS events_count,
        (SELECT COUNT(*) FROM visits) AS visits_count,
        (SELECT ROUND(AVG(score), 1) FROM ratings) AS average_score
"""

# Посещения и средняя оценка по категориям мероприятий
BY_CATEGORY_SQL = """
    SELECT
        events.category,
        COUNT(visits.id) AS visits_count,
        ROUND(AVG(ratings.score), 1) AS average_score
    FROM events
    LEFT JOIN visits
        ON visits.event_id = events.id
    LEFT JOIN ratings
        ON ratings.visit_id = visits.id
    GROUP BY events.category
    ORDER BY visits_count DESC
"""

# Категории, в которых больше заданного числа посещений
POPULAR_SQL = """
    SELECT
        events.category,
        COUNT(visits.id) AS visits_count
    FROM events
    JOIN visits
        ON visits.event_id = events.id
    GROUP BY events.category
    HAVING COUNT(visits.id) > ?
    ORDER BY visits_count DESC
"""

MIN_POPULAR_VISITS = 1


# Страница /visits/: список посещений из базы данных
def visits(request: HttpRequest) -> HttpResponse:
    context = {
        "visits": fetch_all(VISITS_SQL),
    }
    return render(request, "visits/visit_list.html", context)


# Страница /visits/statistics/: подсчеты и группировка средствами SQL
def statistics(request: HttpRequest) -> HttpResponse:
    context = {
        "totals": fetch_one(TOTALS_SQL),
        "categories": fetch_all(BY_CATEGORY_SQL),
        "popular": fetch_all(POPULAR_SQL, (MIN_POPULAR_VISITS,)),
        "min_visits": MIN_POPULAR_VISITS,
    }
    return render(request, "visits/statistics.html", context)


# Страница /visits/<id>/: карточка посещения, иначе ответ 404
def visit_detail(request: HttpRequest, visit_id: int) -> HttpResponse:
    visit = fetch_one(VISIT_SQL, (visit_id,))
    context = {
        "visit": visit,
    }
    return render(request, "visits/visit_detail.html", context,
                  status=404 if visit is None else 200)
