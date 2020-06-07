from django.urls import path
from . import views
from . import charts_data


urlpatterns = [
    path("", views.statistics, name="statistics_and_charts-home"),
    path("data/", views.get_statistics_data, name="get_statistics_data")
]