from django.urls import path
from . import views

urlpatterns = [
    path("", views.salaryprediction, name="salary_prediction-home"),
]