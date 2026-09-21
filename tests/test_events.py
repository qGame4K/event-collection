from datetime import date

import pytest

from models.events import (add_event, find_events, is_past_event,
                           sort_events_by_date)


def test_add_event():
    events = []
    event = add_event(events, "Концерт", " Концерт ", date(2026, 9, 12))
    assert event["id"] == 1
    assert event["category"] == "концерт"
    assert event["date"] == "2026-09-12"


def test_add_event_without_title():
    with pytest.raises(ValueError):
        add_event([], "   ", "концерт", date(2026, 9, 12))


def test_is_past_event():
    event = {"id": 1, "title": "Концерт", "date": "2026-09-12"}
    assert is_past_event(event, date(2026, 9, 21))
    assert not is_past_event(event, date(2026, 9, 1))


def test_find_events():
    events = []
    add_event(events, "Фестиваль уличной еды", "фестиваль", date(2026, 9, 5))
    add_event(events, "Концерт оркестра", "концерт", date(2026, 9, 12))
    assert find_events(events, "ФЕСТ") == [events[0]]


def test_sort_events_by_date():
    events = []
    add_event(events, "Выставка", "выставка", date(2026, 10, 10))
    add_event(events, "Концерт", "концерт", date(2026, 9, 12))
    titles = [event["title"] for event in sort_events_by_date(events)]
    assert titles == ["Концерт", "Выставка"]
