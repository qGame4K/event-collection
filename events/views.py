"""Страницы мероприятий: список и карточка мероприятия."""

from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.events import find_event_by_id, sort_events_by_date
from storage import EVENTS_FILE, load_events


# Страница /events/: список мероприятий из data/events.json
def events(request: HttpRequest) -> HttpResponse:
    context = {
        "events": sort_events_by_date(load_events(EVENTS_FILE)),
    }
    return render(request, "events/event_list.html", context)


# Страница /events/<id>/: карточка мероприятия, иначе ответ 404
def event_detail(request: HttpRequest, event_id: int) -> HttpResponse:
    event = find_event_by_id(load_events(EVENTS_FILE), event_id)
    context = {
        "event": event,
        "passed": event.is_past(date.today()) if event else False,
    }
    return render(request, "events/event_detail.html", context,
                  status=404 if event is None else 200)
