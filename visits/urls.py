from django.urls import path

from . import views

app_name = "visits"

urlpatterns = [
    path("", views.visits, name="list"),
    path("<int:visit_id>/", views.visit_detail, name="detail"),
]
