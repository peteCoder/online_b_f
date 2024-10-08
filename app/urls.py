from django.urls import path
from .views import home as dasboard_home, main_home, register, login
urlpatterns = [
    path('', dasboard_home, name="dashboard_home"),
    path('home/', main_home, name="main_home"),
    path('login/', login, name="login"),
    path('register/', register, name="register"),
]



