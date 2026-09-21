import pytest

from ratings import average_score, format_score, get_rating, rate_event


def test_rate_event():
    ratings = []
    rate_event(ratings, 1, "5")
    assert get_rating(ratings, 1) == 5


def test_rate_event_updates_score():
    ratings = []
    rate_event(ratings, 1, "5")
    rate_event(ratings, 1, "3")
    assert len(ratings) == 1
    assert get_rating(ratings, 1) == 3


def test_rate_event_invalid_input():
    with pytest.raises(ValueError):
        rate_event([], 1, "десять")
    with pytest.raises(ValueError):
        rate_event([], 1, "7")


def test_average_score():
    ratings = []
    rate_event(ratings, 1, "5")
    rate_event(ratings, 2, "4")
    assert average_score(ratings) == 4.5
    assert average_score([]) == 0.0


def test_format_score():
    assert format_score(0) == "не выставлена"
    assert format_score(4) == "★★★★☆ 4/5 — понравилось"
