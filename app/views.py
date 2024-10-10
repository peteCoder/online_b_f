from django.shortcuts import render
from .models import Account, Transaction

# Create your views here.
def home(request):
    return render(request, "dashboard/index.html", {})


def main_home(request):
    return render(request, "main/index.html", {})



def login(request):
    return render(request, "dashboard/login.html", {})



def register(request):
    return render(request, "dashboard/register.html", {})





def chartpage(request):
    return render(request, "dashboard/charts-chartjs.html", {})


def transactions(request):
    transaction_records = Transaction.objects.all()
    return render(request, "dashboard/transactions.html", {"transactions": transaction_records})


def transfer_funds(request):
    transaction_records = Transaction.objects.all()
    
    return render(request, "dashboard/transfer_funds.html", {})

def loans(request):
    return render(request, "dashboard/loan.html", {})

def profile(request):
    return render(request, "dashboard/profile.html", {})

def support_page(request):
    return render(request, "dashboard/support_page.html", {})


def account_details(request, pk):
    return render(request, "dashboard/account_details.html", {})

def accounts_list(request):

    accounts = Account.objects.all()

    return render(request, "dashboard/account_list.html", {"accounts": accounts})








