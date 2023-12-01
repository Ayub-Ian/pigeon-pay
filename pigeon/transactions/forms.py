from .models import Product, Category, Transaction
from django.forms import ModelForm

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'initiator_role']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['transaction']