from django import forms

class MpesaSTKForm(forms.Form):
    phone_number = forms.CharField()
    amount = forms.CharField()