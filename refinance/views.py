from django.http import HttpResponse

from rest_framework import viewsets, serializers
from .models import Transaction, Account, Bank, Category


def index(request):
    return HttpResponse('Foo')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bank
        fields = ('name', 'account_set')


class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('type', 'description', 'bank')


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ('account', 'posted_date', 'description', 'amount', 'category',
                  'transaction_date', 'address', 'reference_number')


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
