from django.shortcuts import render
from .models import Account, Transaction, Loan, Profile

from django.contrib.auth import get_user_model

from django.db.models import Sum, Count
from django.utils import timezone
from collections import defaultdict
import calendar
from django.db.models.functions import ExtractMonth


User = get_user_model()

def get_monthly_transactions(account_type, year):
    transactions = Transaction.objects.filter(
        from_account__account_type=account_type,
        timestamp__year=year
    ).annotate(month=ExtractMonth('timestamp')).values('month').annotate(total=Sum('amount')).order_by('month')

    monthly_data = defaultdict(lambda: 0)  # Default to 0 if no data for a month
    for transaction in transactions:
        monthly_data[transaction['month']] = transaction['total']

    # Return data as list of amounts for each month
    return [int(monthly_data[month]) for month in range(1, 13)]





# Create your views here.
def home(request):
    # user = User.objects.filter(email=request.user.email).first()
    # print(user.email)

    profile = Profile.objects.get(user=request.user)

    accounts = Account.objects.filter(customer=profile).all()
    loans = Loan.objects.filter(customer=profile)


    account_model_meta = {
        'model_name': Account._meta.model_name.upper(),  # Account model name
    }
    loan_model_meta = {
        'model_name': Loan._meta.model_name.upper(),  # Loan model name
    }



    has_loan = loans.count() > 0

    current_year = timezone.now().year

    checking_data = get_monthly_transactions('CHECKING', current_year)
    savings_data = get_monthly_transactions('SAVINGS', current_year)

    print("CHECKING DATA: ", checking_data)
    print("SAVING DATA: ", savings_data)
    print("MONTHS: ", list(calendar.month_abbr[1:]))

    return render(request, "dashboard/major/index.html", {

        'accounts': accounts,
        "loan": loans.first(),
        "has_loan": has_loan,

        # Labels
        "account_model_meta": account_model_meta,
        "loan_model_meta": loan_model_meta,

        'checking_data': checking_data,
        'savings_data': savings_data,
        'months': list(calendar.month_abbr[1:]),


    })


def main_home(request):
    accounts = Account.objects.all()

    account_model_meta = {
        'model_name': Account._meta.model_name,  # Account model name
        'app_label': Account._meta.app_label,    # App name
    }

    return render(request, "main/index.html", {
        'accounts': accounts,
        "account_model_meta": account_model_meta,
    })



def login(request):
    return render(request, "dashboard/major/login.html", {})



def register(request):
    return render(request, "dashboard/major/register.html", {})





def chartpage(request):
    return render(request, "dashboard/major/charts-chartjs.html", {})


def transactions(request):
    transaction_records = Transaction.objects.all()
    return render(request, "dashboard/major/transactions.html", {"transactions": transaction_records})


def transfer_funds(request):
    transaction_records = Transaction.objects.all()
    
    return render(request, "dashboard/major/transfer_funds.html", {})

def loans(request):
    return render(request, "dashboard/major/loan.html", {})

def profile(request):
    return render(request, "dashboard/major/profile.html", {})

def support_page(request):
    return render(request, "dashboard/major/support_page.html", {})


def account_details(request, pk):
    return render(request, "dashboard/major/account_details.html", {})

def accounts_list(request):

    accounts = Account.objects.all()

    return render(request, "dashboard/major/account_list.html", {"accounts": accounts})








