from django.shortcuts import render, redirect
from .models import User
from .forms import UserRegistrationForm, VerifyForm
from django.contrib.auth.decorators import login_required
from .verify import send_otp, check_otp
from .decorators import verification_required

@login_required
@verification_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def register(request):
    template_name = 'accounts/register.html'
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password1'])
            # Save the User object
            new_user.save()
            send_otp(form.cleaned_data.get('phone'))
            return redirect("dashboard")
    return render(request, template_name, {'form': form})


@login_required
def verify_code(request):
    template_name = 'accounts/verify.html'
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if check_otp(request.user.phone, code):
                request.user.is_verified = True
                request.user.save()
                return redirect('dashboard')
    else:
        form = VerifyForm()
    return render(request, template_name, {'form': form})