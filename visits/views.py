"""Страницы посещений: список и карточка посещения."""

from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models import Visit
from models.visits import find_visit_by_id
from storage import (EVENTS_FILE, RATINGS_FILE, USERS_FILE, VISITS_FILE,
                     load_events, load_ratings, load_users, load_visits)


# Загружает посещения вместе с пользователями, мероприятиями и оценками
def load_all_visits() -> list[Visit]:
    users = load_users(USERS_FILE)
    events = load_events(EVENTS_FILE)
    all_visits = load_visits(VISITS_FILE, users, events)
    load_ratings(RATINGS_FILE, all_visits)
    return all_visits


# Страница /visits/: список посещений из data/visits.json
def visits(request: HttpRequest) -> HttpResponse:
    context = {
        "visits": load_all_visits(),
    }
    return render(request, "visits/visit_list.html", context)


# Страница /visits/<id>/: карточка посещения, иначе ответ 404
def visit_detail(request: HttpRequest, visit_id: int) -> HttpResponse:
    visit = find_visit_by_id(load_all_visits(), visit_id)
    context = {
        "visit": visit,
        "days": visit.days_passed(date.today()) if visit else 0,
    }
    return render(request, "visits/visit_detail.html", context,
                  status=404 if visit is None else 200)
