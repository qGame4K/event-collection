from datetime import date

import pytest

from models import Event, User, Visit
from models.visits import (add_visit, collect_ratings, get_user_visits,
                           has_visit, remove_visit)

TODAY = date(2026, 9, 27)


def make_user() -> User:
    return User(1, "Иван", "ivan@example.com")


def make_event(event_date: date = date(2026, 9, 12)) -> Event:
    return Event(1, "Концерт", "концерт", event_date)


def test_visit_links_user_and_event():
    user = make_user()
    event = make_event()
    visit = Visit(1, user, event)
    assert visit.user is user
    assert visit.event is event
    assert visit.rating is None


def test_visit_str():
    visit = Visit(1, make_user(), make_event())
    assert str(visit) == "Посещение №1: Концерт (концерт)"


def test_visit_to_data():
    visit = Visit(1, make_user(), make_event())
    assert visit.to_data() == {"id": 1, "user_id": 1, "event_id": 1}


def test_visit_from_data():
    users = [make_user()]
    events = [make_event()]
    data = {"id": 1, "user_id": 1, "event_id": 1}
    visit = Visit.from_data(data, users, events)
    assert visit.user is users[0]
    assert visit.event is events[0]


def test_visit_from_data_without_user():
    data = {"id": 1, "user_id": 99, "event_id": 1}
    assert Visit.from_data(data, [], [make_event()]) is None


def test_add_visit_creates_object():
    visits = []
    user, event = make_user(), make_event()
    visit = add_visit(visits, user, event, TODAY)
    assert visits == [visit]
    assert has_visit(visits, user, event)


def test_add_visit_to_future_event():
    with pytest.raises(ValueError):
        add_visit([], make_user(), make_event(date(2026, 10, 10)), TODAY)


def test_duplicate_visit_forbidden():
    visits = []
    user, event = make_user(), make_event()
    add_visit(visits, user, event, TODAY)
    with pytest.raises(ValueError):
        add_visit(visits, user, event, TODAY)


def test_get_user_visits():
    visits = []
    event = make_event()
    add_visit(visits, make_user(), event, TODAY)
    anna = User(2, "Анна", "anna@example.com")
    add_visit(visits, anna, event, TODAY)
    assert len(get_user_visits(visits, anna)) == 1


def test_remove_visit():
    visits = []
    visit = add_visit(visits, make_user(), make_event(), TODAY)
    assert remove_visit(visits, visit.id)
    assert not remove_visit(visits, visit.id)


def test_visit_rate_replaces_old_score():
    visit = Visit(1, make_user(), make_event())
    visit.rate("5", 1)
    assert visit.rating.score == 5
    visit.rate("3", 2)
    assert visit.rating.id == 1
    assert visit.rating.score == 3


def test_visit_rate_out_of_scale():
    visit = Visit(1, make_user(), make_event())
    with pytest.raises(ValueError):
        visit.rate("7", 1)


def test_visit_days_passed_and_card():
    visit = Visit(1, make_user(), make_event())
    visit.rate("5", 1)
    assert visit.days_passed(TODAY) == 15
    card = visit.card(TODAY)
    assert "15 дн. назад" in card
    assert "5/5" in card


def test_collect_ratings():
    visits = [Visit(1, make_user(), make_event()),
              Visit(2, make_user(), make_event())]
    visits[0].rate("4", 1)
    assert len(collect_ratings(visits)) == 1
