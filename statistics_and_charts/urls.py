from django.urls import path
from . import views


urlpatterns = [
    path("", views.statistics, name="statistics_and_charts-home"),
]