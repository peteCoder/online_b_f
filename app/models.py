from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from django.utils import timezone
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for the bank app where email is the unique identifier for authentication.
    """

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    ssn = models.CharField(max_length=50)
    
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Users"
        verbose_name = "User"

class Customer(models.Model):
    EMPLOYMENT_STATUS = [
        ("employed", "employed"),
        ("self-employed", "self-employed"),
        ("unemployed", "unemployed"),
    ]
    PREFERRED_ACCOUNT_TYPE = [
        ('CHECKING', 'Checking'),
        ('SAVINGS', 'Savings'),
        ('MONEY_MARKET', 'Money Market'),
        ('CD', 'Certificate of Deposit (CD)'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    annual_income = models.CharField(max_length=100)
    employment_status = models.CharField(max_length=100, choices=EMPLOYMENT_STATUS)
    preferred_account_type = models.CharField(max_length=100, choices=PREFERRED_ACCOUNT_TYPE)


    def __str__(self):
        return self.user.username


class Account(models.Model):
    ACCOUNT_TYPES = (
        ('CHECKING', 'Checking'),
        ('SAVINGS', 'Savings'),
        ('MONEY_MARKET', 'Money Market'),
        ('CD', 'Certificate of Deposit (CD)'),
    )

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.user.email} - {self.account_type} ({self.account_number})"

    

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
    )

    from_account = models.ForeignKey(Account, related_name='from_transactions', on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name='to_transactions', on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} from {self.from_account.account_number}"


class Card(models.Model):
    CARD_TYPES = (
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, unique=True)
    card_type = models.CharField(max_length=6, choices=CARD_TYPES)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.card_type} card for {self.customer.user.username}"

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan for {self.customer.user.email} - {self.amount}"





