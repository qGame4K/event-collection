"""Страницы мероприятий: список и карточка мероприятия."""

from datetime import date

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models.events import find_event_by_id, sort_events_by_date
from storage import EVENTS_FILE, load_events


# Страница /events/: список мероприятий из data/events.json
def events(request: HttpRequest) -> HttpResponse:
    items = ""
    for event in sort_events_by_date(load_events(EVENTS_FILE)):
        when = event.date.strftime("%d.%m.%Y")
        link = f'<a href="/events/{event.id}/">{event.title}</a>'
        items += (f'<li class="list-group-item">{link}'
                  f' — {when}, {event.category}</li>')
    content = f"""
<h1>Мероприятия</h1>
<ul class="list-group">{items}</ul>
"""
    return HttpResponse(page("Event Collection — мероприятия", content))


# Страница /events/<id>/: карточка мероприятия, иначе ответ 404
def event_detail(request: HttpRequest, event_id: int) -> HttpResponse:
    event = find_event_by_id(load_events(EVENTS_FILE), event_id)
    if event is None:
        content = """
<h1 class="text-danger">Мероприятие не найдено</h1>
<a href="/events/" class="btn btn-outline-secondary">
к списку мероприятий</a>
"""
        return HttpResponse(page("Мероприятие не найдено", content),
                            status=404)
    passed = event.is_past(date.today())
    status = "уже прошло" if passed else "еще не прошло"
    badge = "bg-secondary" if passed else "bg-success"
    when = event.date.strftime("%d.%m.%Y")
    content = f"""
<div class="card">
<div class="card-body">
<h5 class="card-title">{event.title}</h5>
<p class="card-text">Номер: {event.id}</p>
<p class="card-text">Категория: {event.category}</p>
<p class="card-text">Дата: {when}
<span class="badge {badge}">{status}</span></p>
<a href="/visits/" class="btn btn-outline-primary me-2">Посещения</a>
<a href="/events/" class="btn btn-outline-secondary">
к списку мероприятий</a>
</div>
</div>
"""
    return HttpResponse(page(event.title, content))
