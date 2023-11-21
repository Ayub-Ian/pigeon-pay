from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import re

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    phone = forms.CharField(label="Phone number", max_length=20, required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name','email', 'phone']
    
    def clean_phone(self):
        """Validates number start with +254 or 0, then 9 digits"""
        cd = self.cleaned_data
        number = cd['phone']
        number_pattern = re.compile(r'^(?:\+254|0)\d{9}$')
        result = number_pattern.match(number)
        if result:
            if number.startswith('0'): 
                return '+254' + number[1:]
            return number
        
class VerifyForm(forms.Form):
    code = forms.CharField(label="Verification code",max_length=8, required=True, help_text='Enter code')