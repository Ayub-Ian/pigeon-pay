from django.urls import path
from . import views
 
app_name = 'transactions'

urlpatterns = [
    path('create/',views.transaction_create, name="transaction_create")
]