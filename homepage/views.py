"""Главная страница проекта."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Главная страница: описание проекта и переходы в разделы
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "homepage/index.html")
