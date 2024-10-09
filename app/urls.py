from django.urls import path
from .views import home as dasboard_home, main_home, register, login, chartpage
urlpatterns = [
    path('', dasboard_home, name="dashboard_home"),
    path('home/', main_home, name="main_home"),
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('chart/', chartpage, name="chartpage"),
]



