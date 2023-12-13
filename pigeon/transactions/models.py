from django.db import models
from accounts.models import Buyer, Seller, User
from django.urls import reverse



class Transaction(models.Model):
    PENDING = 'P'
    IN_PROGRESS = 'IP'
    COMPLETED = 'C'
    CANCELED = 'X'
    ACTION_REQUIRED = 'AR'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
        (ACTION_REQUIRED, 'Action Required'),
    ]

    amount = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    url = models.CharField(max_length=255, null=True, blank=True)
    buyer = models.ForeignKey(Buyer,
                              on_delete=models.SET_NULL,
                              related_name="buyer_transactions",
                              null=True,
                              blank=True)
    seller = models.ForeignKey(Seller,
                               on_delete=models.SET_NULL,
                               related_name='seller_transactions',
                               null=True,
                               blank=True)
    initiator = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='initiated_transactions')
    initiator_role = models.CharField(max_length=10, choices=[('buyer', 'Buyer'), ('seller', 'Seller')])
    action_description = models.TextField(blank=True, null=True)  
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)


    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("transactions:transaction_detail",args = [self.id])

class Category(models.Model):
    name = models.CharField(max_length=200)
  
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    inspection_period = models.IntegerField(default=1, null=False, blank=False)
    transaction = models.ForeignKey(Transaction,
                                related_name='products',
                                on_delete=models.CASCADE
                                )
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id'])
        ]

    def __str__(self) -> str:
        return self.name


class TransactionHistory(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action_timestamp = models.DateTimeField(auto_now_add=True)
    action_description = models.TextField()