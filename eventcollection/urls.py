"""Маршруты проекта: адреса распределены между приложениями."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("events/", include("events.urls")),
    path("visits/", include("visits.urls")),
]
