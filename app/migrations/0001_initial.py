# Generated by Django 4.2.9 on 2024-10-17 13:46

import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('address', models.TextField()),
                ('ssn', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('annual_income', models.CharField(blank=True, max_length=100, null=True)),
                ('employment_status', models.CharField(blank=True, choices=[('employed', 'employed'), ('self-employed', 'self-employed'), ('unemployed', 'unemployed')], max_length=100, null=True)),
                ('preferred_account_type', models.CharField(blank=True, choices=[('CHECKING', 'Checking'), ('SAVINGS', 'Savings'), ('MONEY_MARKET', 'Money Market'), ('CD', 'Certificate of Deposit (CD)')], max_length=100, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile/images')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=20, unique=True)),
                ('account_type', models.CharField(choices=[('CHECKING', 'Checking'), ('SAVINGS', 'Savings')], max_length=20)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bank_name', models.CharField(blank=True, default='FirstCitzen Bank', max_length=200, null=True)),
                ('location', models.CharField(blank=True, default=app.models.change_account_location, max_length=500, null=True)),
                ('ach_routing', models.CharField(blank=True, max_length=200, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_holder_name', models.CharField(blank=True, max_length=200, null=True)),
                ('account_number', models.CharField(blank=True, max_length=200, null=True)),
                ('ach_routing', models.CharField(blank=True, max_length=200, null=True)),
                ('account_type', models.CharField(blank=True, choices=[('CHECKING', 'Checking'), ('SAVINGS', 'Savings')], max_length=200, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=200, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('from_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfered_from', to='app.account')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('DEPOSIT', 'Deposit'), ('WITHDRAWAL', 'Withdrawal'), ('TRANSFER', 'Transfer')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('from_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_transactions', to='app.account')),
                ('to_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_transactions', to='app.account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('loan_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField()),
                ('is_paid', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Loan',
                'verbose_name_plural': 'Loans',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16, unique=True)),
                ('card_type', models.CharField(choices=[('DEBIT', 'Debit'), ('CREDIT', 'Credit')], max_length=6)),
                ('expiry_date', models.DateField()),
                ('cvv', models.CharField(max_length=3)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.account')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Card',
                'verbose_name_plural': 'Cards',
            },
        ),
    ]
