# home/urls.py

from django.urls import path
from home import views

urlpatterns = [
    path("", views.home_index, name="project_index"),
    # path("<int:pk>/", views.project_detail, name="project_detail"),
]