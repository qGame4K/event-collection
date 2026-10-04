from django.urls import path

from . import views

urlpatterns = [
    path("", views.visits, name="visits"),
    path("<int:visit_id>/", views.visit_detail, name="visit_detail"),
]
