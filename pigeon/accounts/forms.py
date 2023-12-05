from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}
        ),
        label='Email address',
        max_length=100
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}
        ),
        label='Password',
        max_length = 100
    )