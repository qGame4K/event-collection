"""Оценки: впечатления пользователя о посещенных мероприятиях."""

from utils import find_by, next_id

MIN_SCORE = 1
MAX_SCORE = 5


# Выставляет оценку посещению: проверяет ввод и сохраняет число от 1 до 5
def rate_event(ratings: list[dict], visit_id: int, score_text: str) -> dict:
    try:
        score = int(score_text)
    except ValueError:
        raise ValueError("Оценка должна быть целым числом.") from None
    if not MIN_SCORE <= score <= MAX_SCORE:
        raise ValueError(f"Оценка должна быть от {MIN_SCORE} до {MAX_SCORE}.")

    rating = find_by(ratings, "visit_id", visit_id)
    if rating is not None:
        rating["score"] = score
        return rating
    rating = {"id": next_id(ratings), "visit_id": visit_id, "score": score}
    ratings.append(rating)
    return rating


# Возвращает оценку посещения или 0, если оценки еще нет
def get_rating(ratings: list[dict], visit_id: int) -> int:
    rating = find_by(ratings, "visit_id", visit_id)
    return 0 if rating is None else rating["score"]


# Удаляет оценку посещения, если она есть
def remove_rating(ratings: list[dict], visit_id: int) -> None:
    rating = find_by(ratings, "visit_id", visit_id)
    if rating is not None:
        ratings.remove(rating)


# Считает среднюю оценку с точностью до десятых (0, если оценок нет)
def average_score(ratings: list[dict]) -> float:
    if not ratings:
        return 0.0
    total = sum(rating["score"] for rating in ratings)
    return round(total / len(ratings), 1)


# Показывает оценку звездами с пояснением или сообщает, что ее нет
def format_score(score: int) -> str:
    if score == 0:
        return "не выставлена"
    stars = "★" * score + "☆" * (MAX_SCORE - score)
    if score >= 4:
        verdict = "понравилось"
    elif score == 3:
        verdict = "нормально"
    else:
        verdict = "не понравилось"
    return f"{stars} {score}/{MAX_SCORE} — {verdict}"
