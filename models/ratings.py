"""Оценки: класс Rating и функции работы с оценками посещений."""

MIN_SCORE = 1
MAX_SCORE = 5


# Оценка посещения по шкале от 1 до 5
class Rating:
    # Создает оценку и проверяет, что балл входит в шкалу
    def __init__(self, rating_id: int, score: int) -> None:
        if not MIN_SCORE <= score <= MAX_SCORE:
            raise ValueError(
                f"Оценка должна быть от {MIN_SCORE} до {MAX_SCORE}.")
        self.id = rating_id
        self.score = score

    # Превращает введенную строку в целое число (метод класса, без объекта)
    @staticmethod
    def parse_score(score_text: str) -> int:
        try:
            return int(score_text)
        except ValueError:
            raise ValueError("Оценка должна быть целым числом.") from None

    # Оценка звездами; пишется без скобок: rating.stars
    @property
    def stars(self) -> str:
        return "★" * self.score + "☆" * (MAX_SCORE - self.score)

    # Создает оценку из данных JSON
    @classmethod
    def from_data(cls, data: dict) -> "Rating":
        return cls(data["id"], data["score"])

    # Превращает оценку в данные для JSON (связь с посещением — по номеру)
    def to_data(self, visit_id: int) -> dict:
        return {"id": self.id, "visit_id": visit_id, "score": self.score}

    # Строковое представление оценки
    def __str__(self) -> str:
        if self.score >= 4:
            verdict = "понравилось"
        elif self.score == 3:
            verdict = "нормально"
        else:
            verdict = "не понравилось"
        return f"{self.stars} {self.score}/{MAX_SCORE} — {verdict}"


# Считает среднюю оценку с точностью до десятых (0, если оценок нет)
def average_score(ratings: list[Rating]) -> float:
    if not ratings:
        return 0.0
    total = sum(rating.score for rating in ratings)
    return round(total / len(ratings), 1)
