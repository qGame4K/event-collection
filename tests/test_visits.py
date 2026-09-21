from datetime import date

import pytest

from models.visits import (add_visit, get_user_visits, has_visit,
                           remove_visit, show_visit_card)

TODAY = date(2026, 9, 21)
PAST_EVENT = {"id": 1, "title": "Концерт", "category": "концерт",
              "date": "2026-09-12"}
FUTURE_EVENT = {"id": 2, "title": "Выставка", "category": "выставка",
                "date": "2026-10-10"}


def test_add_visit():
    visits = []
    visit = add_visit(visits, 1, PAST_EVENT, TODAY)
    assert visit == {"id": 1, "user_id": 1, "event_id": 1}
    assert has_visit(visits, 1, 1)


def test_add_visit_to_future_event():
    with pytest.raises(ValueError):
        add_visit([], 1, FUTURE_EVENT, TODAY)


def test_duplicate_visit_forbidden():
    visits = []
    add_visit(visits, 1, PAST_EVENT, TODAY)
    with pytest.raises(ValueError):
        add_visit(visits, 1, PAST_EVENT, TODAY)


def test_get_user_visits():
    visits = []
    add_visit(visits, 1, PAST_EVENT, TODAY)
    add_visit(visits, 2, PAST_EVENT, TODAY)
    assert len(get_user_visits(visits, 2)) == 1


def test_remove_visit():
    visits = []
    visit = add_visit(visits, 1, PAST_EVENT, TODAY)
    assert remove_visit(visits, visit["id"])
    assert not remove_visit(visits, visit["id"])


def test_show_visit_card(capsys):
    visit = {"id": 1, "user_id": 1, "event_id": 1}
    ratings = [{"id": 1, "visit_id": 1, "score": 5}]
    show_visit_card(visit, [PAST_EVENT], ratings, TODAY)
    output = capsys.readouterr().out
    assert "9 дн. назад" in output
    assert "5/5" in output
