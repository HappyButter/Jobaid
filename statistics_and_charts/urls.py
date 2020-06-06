from django.urls import path
from . import views
from . import charts_data


urlpatterns = [
    path("", views.statistics, name="statistics_and_charts-home"),
    path("recalculate_statistics/", views.recalculate_statistics, name="charts_data")
]