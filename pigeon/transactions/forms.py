from .models import Product, Transaction
from django import forms

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'initiator_role']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['transaction']

class AcceptanceForm(forms.Form):
    transaction = forms.ModelChoiceField(
        queryset=Transaction.objects.all(),
        widget=forms.HiddenInput)
