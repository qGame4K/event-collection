from datetime import date

import pytest

from models import Event
from models.events import (add_event, find_events, get_categories,
                           sort_events_by_date)

TODAY = date(2026, 9, 27)


def test_event_creation():
    event = Event(1, "Концерт", "концерт", date(2026, 9, 12))
    assert event.id == 1
    assert event.title == "Концерт"
    assert event.date == date(2026, 9, 12)


def test_event_is_past():
    event = Event(1, "Концерт", "концерт", date(2026, 9, 12))
    assert event.is_past(TODAY)
    assert not event.is_past(date(2026, 9, 1))


def test_event_str():
    event = Event(1, "Концерт", "концерт", date(2026, 9, 12))
    assert str(event) == "1. 12.09.2026 Концерт (концерт)"


def test_event_from_data():
    data = {"id": 1, "title": "Концерт", "category": "концерт",
            "date": "2026-09-12"}
    event = Event.from_data(data)
    assert event.date == date(2026, 9, 12)
    assert event.to_data() == data


def test_add_event_creates_object():
    events = []
    event = add_event(events, "Концерт", " Концерт ", date(2026, 9, 12))
    assert isinstance(event, Event)
    assert event.category == "концерт"
    assert events == [event]


def test_add_event_without_title():
    with pytest.raises(ValueError):
        add_event([], "   ", "концерт", date(2026, 9, 12))


def test_find_events():
    events = []
    add_event(events, "Фестиваль уличной еды", "фестиваль", date(2026, 9, 5))
    add_event(events, "Концерт оркестра", "концерт", date(2026, 9, 12))
    assert find_events(events, "ФЕСТ") == [events[0]]


def test_sort_events_by_date():
    events = []
    add_event(events, "Выставка", "выставка", date(2026, 10, 10))
    add_event(events, "Концерт", "концерт", date(2026, 9, 12))
    titles = [event.title for event in sort_events_by_date(events)]
    assert titles == ["Концерт", "Выставка"]


def test_get_categories():
    events = []
    add_event(events, "Выставка", "выставка", date(2026, 10, 10))
    add_event(events, "Концерт", "концерт", date(2026, 9, 12))
    assert get_categories(events) == {"выставка", "концерт"}
