"""Страницы посещений: список и карточка посещения."""

from datetime import date

from django.http import HttpRequest, HttpResponse

from homepage.views import page
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
    items = ""
    for visit in load_all_visits():
        score = "без оценки" if visit.rating is None else visit.rating.stars
        badge = "bg-secondary" if visit.rating is None else "bg-success"
        link = f'<a href="/visits/{visit.id}/">{visit.event.title}</a>'
        items += f"""
<li class="list-group-item d-flex justify-content-between">
{link} — {visit.user.name}
<span class="badge {badge}">{score}</span></li>"""
    content = f"""
<h1>Посещения</h1>
<ul class="list-group">{items}</ul>
"""
    return HttpResponse(page("Event Collection — посещения", content))


# Страница /visits/<id>/: карточка посещения, иначе ответ 404
def visit_detail(request: HttpRequest, visit_id: int) -> HttpResponse:
    visit = find_visit_by_id(load_all_visits(), visit_id)
    if visit is None:
        content = """
<h1 class="text-danger">Посещение не найдено</h1>
<a href="/visits/" class="btn btn-outline-secondary">
к списку посещений</a>
"""
        return HttpResponse(page("Посещение не найдено", content),
                            status=404)
    days = visit.days_passed(date.today())
    rating = "не выставлена" if visit.rating is None else str(visit.rating)
    when = visit.event.date.strftime("%d.%m.%Y")
    content = f"""
<div class="card">
<div class="card-body">
<h5 class="card-title">Посещение №{visit.id}</h5>
<p class="card-text">Мероприятие:
<a href="/events/{visit.event.id}/">{visit.event.title}</a></p>
<p class="card-text">Дата: {when} ({days} дн. назад)</p>
<p class="card-text">Пользователь: {visit.user.name}</p>
<p class="card-text">Оценка: {rating}</p>
<a href="/visits/" class="btn btn-outline-secondary">
к списку посещений</a>
</div>
</div>
"""
    return HttpResponse(page(f"Посещение №{visit.id}", content))
