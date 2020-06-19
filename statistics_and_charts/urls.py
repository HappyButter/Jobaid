from django.urls import path
from .views import statistics, get_statistics_data, get_pie_charts_data, get_bar_charts_data

urlpatterns = [
    path("", statistics, name="statistics_and_charts-home"),
    path("data/", get_statistics_data, name="get_statistics_data"),
    path("data/pie/", get_pie_charts_data, name="get_pie_charts_data"),
    path("data/bar/", get_bar_charts_data, name="get_bar_charts_data")     
]