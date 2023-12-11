from django.urls import path
from . import views
 
app_name = 'transactions'

urlpatterns = [
    path('create/',views.transaction_create, name="transaction_create"),
    path('', views.transaction_list, name="transaction_list"),
    path('<int:id>/detail', views.transaction_detail, name="transaction_detail"),
    path('<int:id>/preview', views.transaction_preview, name="transaction_preview"),
    path('accept-transaction/',views.TransactionAcceptanceView.as_view(), name="user_accept_transaction")
]