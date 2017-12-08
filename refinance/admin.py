from decimal import Decimal
from django import forms
from django.contrib import admin
from django.shortcuts import render

from dateutil import parser
from django_object_actions import DjangoObjectActions

from .models import Category, Bank, Account, Transaction, Expense, Deposit


def bulk_add_transactions(input_data, account_id):
    account = Account.objects.get(id=account_id)
    parsed_data = [row.split('\t') for row in input_data.split('\r\n')]

    if account_id == BulkAddForm.CHASE_CC:
        return Transaction.objects.bulk_create([Transaction(
            account=account,
            posted_date=parser.parse(row[0]),
            reference_number=row[1],
            description=row[2],
            address=row[3],
            amount=Decimal(row[4])
        ) for row in parsed_data])

    elif account_id == BulkAddForm.BOFA_CC:
        return Transaction.objects.bulk_create([Transaction(
            account=account,
            transaction_date=parser.parse(row[1]),
            posted_date=parser.parse(row[2]),
            description=row[3],
            amount=Decimal(row[4])
        ) for row in parsed_data])

    elif account_id == BulkAddForm.BOFA_SAVINGS:
        print(parsed_data[0])
        return Transaction.objects.bulk_create([Transaction(
            account=account,
            posted_date=parser.parse(row[0]),
            description=row[1],
            amount=Decimal(row[2])
        ) for row in parsed_data])


class BulkAddForm(forms.Form):
    CHASE_CC = 1
    BOFA_CC = 2
    BOFA_SAVINGS = 3
    ACCOUNT_CHOICES = (
        (CHASE_CC, 'Chase credit card'),
        (BOFA_CC, 'B of A credit card'),
        (BOFA_SAVINGS, 'B of A savings')
    )
    account = forms.ChoiceField(choices=ACCOUNT_CHOICES)
    input = forms.CharField(widget=forms.Textarea)


class TransactionAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('description', 'account', 'posted_date', 'amount')
    list_filter = ('category', 'account')

    def bulk_add(modeladmin, request, queryset):
        if request.method == 'GET':
            data = {'form': BulkAddForm()}
            return render(request, 'refinance/bulk_add.html', data)
        if 'input' in request.POST:
            transactions = bulk_add_transactions(request.POST['input'], int(request.POST['account']))
            modeladmin.message_user(request, '%d transactions added' % len(transactions))

    changelist_actions = ('bulk_add',)


admin.site.register(Category)
admin.site.register(Bank)
admin.site.register(Account)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Expense, TransactionAdmin)
admin.site.register(Deposit, TransactionAdmin)
