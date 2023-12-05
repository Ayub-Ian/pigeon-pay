from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# app_name= 'accounts'

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('register/', views.register, name="register"),
    path('login/', views.LoginView.as_view(), name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('verify/', views.verify_code, name="verify")
]