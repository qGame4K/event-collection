"""Главная страница и общий HTML-каркас всех страниц проекта."""

from django.http import HttpRequest, HttpResponse

BOOTSTRAP = ("https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
             "/dist/css/bootstrap.min.css")


# Собирает HTML-страницу: кодировка, заголовок, Bootstrap и навигация
def page(title: str, content: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{BOOTSTRAP}">
</head>
<body>
<nav class="nav border-bottom mb-3">
<a class="nav-link" href="/">Главная</a>
<a class="nav-link" href="/events/">Мероприятия</a>
<a class="nav-link" href="/visits/">Посещения</a>
</nav>
<main class="container">{content}</main>
</body>
</html>"""


# Главная страница: описание проекта и переходы в разделы
def index(request: HttpRequest) -> HttpResponse:
    content = """
<h1 class="display-5">Event Collection</h1>
<p class="lead">Личная коллекция посещенных мероприятий.</p>
<p>Основные разделы:</p>
<a href="/events/" class="btn btn-primary me-2">Мероприятия</a>
<a href="/visits/" class="btn btn-secondary">Посещения</a>
"""
    return HttpResponse(page("Event Collection", content))
