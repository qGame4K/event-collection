from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.events, name="list"),
    path("search/", views.event_search, name="search"),
    path("<int:event_id>/", views.event_detail, name="detail"),
]
