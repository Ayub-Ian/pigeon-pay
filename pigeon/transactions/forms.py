from .models import Product, Transaction, ProductFile
from django import forms


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['initiator_role', 'title', 'amount', 'category' ]
        widgets = {
            "initiator_role" : forms.RadioSelect( attrs={'class': "role-select"})
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['transaction']

class AcceptanceForm(forms.Form):
    transaction = forms.ModelChoiceField(
        queryset=Transaction.objects.all(),
        widget=forms.HiddenInput)

class ProductFileForm(forms.ModelForm):
    class Meta:
        model = ProductFile
        exclude = ['created', 'updated', 'transaction']

class RecepientDetailsForm(forms.Form):
    email =forms.EmailField()
    name = forms.CharField(max_length=50)