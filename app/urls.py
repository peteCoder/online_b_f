from django.urls import path, include
from .views import home as dasboard_home
urlpatterns = [
    path('', dasboard_home, name="dashboard_home"),
]