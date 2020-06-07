from django.urls import path
from . import views


urlpatterns = [
    path("", views.joboffers, name="joboffers"),
    path("admin/", views.admin, name="admin"),
]