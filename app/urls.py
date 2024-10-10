from django.urls import path
from .views import home as dasboard_home, main_home, profile, support_page, register, loans, transfer_funds, login,account_details, accounts_list, transactions, chartpage
urlpatterns = [
    path('', dasboard_home, name="dashboard_home"),
    path('home/', main_home, name="main_home"),
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('chart/', chartpage, name="chartpage"),
    path('accounts/<int:pk>/', account_details, name="accounts_detail"),
    path('accounts/', accounts_list, name="accounts"),
    path('transactions/', transactions, name="transactions"),
    path('transfer/', transfer_funds, name="transfer_funds"),
    path('loans/', loans, name="loans"),
    path('profile/', profile, name="profile"),
    path('support/', support_page, name="support"),
]



