from django.urls import path
from . import views
 
app_name = 'transactions'

urlpatterns = [
    path('create/',views.transaction_create, name="transaction_create"),
    path('', views.transaction_list, name="transaction_list"),
    path('transaction/<int:id>/', views.transaction_detail, name="transaction_detail")
]