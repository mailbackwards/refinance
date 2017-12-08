from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Account(models.Model):
    SAVINGS = 'S'
    CREDIT = 'C'
    DEBIT = 'D'
    INVESTMENT = 'I'
    TYPE_CHOICES = (
        (SAVINGS, 'Savings'),
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
        (INVESTMENT, 'Investment')
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    description = models.CharField(blank=True, max_length=128, default='')
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT)

    def __str__(self):
        return self.description


class Transaction(models.Model):
    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.PROTECT)
    posted_date = models.DateField()
    description = models.CharField(max_length=512)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, related_name='transactions', null=True, on_delete=models.PROTECT)

    transaction_date = models.DateField(null=True)
    address = models.CharField(blank=True, max_length=512, default='')
    reference_number = models.CharField(blank=True, max_length=256, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ('-posted_date',)
        # to protect from bulk-adding dupes
        unique_together = ('account', 'posted_date', 'description', 'amount')


class TransactionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.is_positive = kwargs.pop('is_positive', None)
        super(TransactionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        lookup = 'gt' if self.is_positive else 'lt'
        return super(TransactionManager, self).get_queryset().filter(**{'amount__%s' % lookup: 0})


class Expense(Transaction):
    objects = TransactionManager(is_positive=False)

    class Meta:
        proxy = True


class Deposit(Transaction):
    objects = TransactionManager(is_positive=True)

    class Meta:
        proxy = True
