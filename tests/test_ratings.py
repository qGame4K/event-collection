import pytest

from models import Rating
from models.ratings import average_score


def test_rating_creation():
    rating = Rating(1, 5)
    assert rating.id == 1
    assert rating.score == 5


def test_rating_out_of_scale():
    with pytest.raises(ValueError):
        Rating(1, 7)


def test_rating_stars():
    assert Rating(1, 4).stars == "★★★★☆"


def test_rating_str():
    assert str(Rating(1, 4)) == "★★★★☆ 4/5 — понравилось"


def test_parse_score():
    assert Rating.parse_score(" 5 ") == 5


def test_parse_score_invalid():
    with pytest.raises(ValueError):
        Rating.parse_score("десять")


def test_rating_from_data():
    data = {"id": 2, "visit_id": 3, "score": 4}
    rating = Rating.from_data(data)
    assert rating.score == 4
    assert rating.to_data(3) == data


def test_average_score():
    assert average_score([Rating(1, 5), Rating(2, 4)]) == 4.5
    assert average_score([]) == 0.0
