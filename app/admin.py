from django.contrib import admin
from .models import CustomUser, Account, Transaction, Loan, Card
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Loan)
admin.site.register(Card)
 




