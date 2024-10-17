from django.shortcuts import render, redirect
from .models import Account, Transaction, Loan

from django.contrib.auth import get_user_model
import json
from django.db.models import Sum, Count
from django.utils import timezone
from collections import defaultdict
import calendar
from django.db.models.functions import ExtractMonth

from django.http import Http404

from .forms import TransferForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SignupForm



User = get_user_model()

def get_monthly_transactions(account_type, year, user):
    transactions = Transaction.objects.filter(
        from_account__account_type=account_type,
        from_account__customer=user,
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

    user = request.user

    if not user.is_authenticated:
        return redirect("login")

    

    # profile = Profile.objects.get(user=request.user)

    accounts = Account.objects.filter(customer=user).all()
    loans = Loan.objects.filter(customer=user)


    account_model_meta = {
        'model_name': Account._meta.model_name.upper(),  # Account model name
    }
    loan_model_meta = {
        'model_name': Loan._meta.model_name.upper(),  # Loan model name
    }



    has_loan = loans.count() > 0

    current_year = timezone.now().year

    checking_data = get_monthly_transactions('CHECKING', current_year, user)
    savings_data = get_monthly_transactions('SAVINGS', current_year, user)
    months_data = list(calendar.month_abbr[1:])

    all_transactions = Transaction.objects.all()

    

    return render(request, "dashboard/major/index.html", {

        'accounts': accounts,
        "loan": loans.first(),
        "has_loan": has_loan,

        # Labels
        "account_model_meta": account_model_meta,
        "loan_model_meta": loan_model_meta,

        'checking_data': json.dumps(checking_data),
        'savings_data': json.dumps(savings_data),
        'months_data': json.dumps(months_data),


    })

def LogoutView(request):
	logout(request)
	return redirect('login')


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


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard_home')  # Change to your dashboard page
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, "main/pages-sign-in.html", {})



def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")
    

    
    if request.method == 'POST':
        print(request.POST)  # Print the POST data to confirm what's being submitted
        print(request.FILES)
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            # This will print the actual form validation errors to the terminal

            for field in form:
                print(f"{field.name}: {field.errors}")  # Print specific field errors
            print("Form is not valid")
            print(form.errors)  # Prints field-specific errors
            print(form.non_field_errors())  # Prints non-field errors if any
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = SignupForm()

    return render(request, "main/pages-sign-up.html", {'form': form})





def chartpage(request):
    return render(request, "dashboard/major/charts-chartjs.html", {})


def transactions(request):
    transaction_records = Transaction.objects.all()
    return render(request, "dashboard/major/transactions.html", {"transactions": transaction_records})


def transfer_funds(request):
    transaction_records = Transaction.objects.all()

    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # redirect to a success page after transfer
    else:
        form = TransferForm()
    
    return render(request, "dashboard/major/transfer_funds.html", {})

def loans(request):
    return render(request, "dashboard/major/loan.html", {})

def profile(request):
    return render(request, "dashboard/major/profile.html", {})

def support_page(request):
    return render(request, "dashboard/major/support_page.html", {})


def account_details(request, pk):
    user = request.user
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        raise Http404
    
    transactions = Transaction.objects.filter(from_account=account, user=user)

    return render(
        request, 
        "dashboard/major/account_details.html", 
        {
            "account": account, 
            "transactions": transactions
        }
    )

def accounts_list(request):

    accounts = Account.objects.all()

    return render(request, "dashboard/major/account_list.html", {"accounts": accounts})








