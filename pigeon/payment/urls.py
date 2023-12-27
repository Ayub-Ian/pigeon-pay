from django.urls import path

from . import views

app_name="payment"

urlpatterns = [
    path("checkout/", views.MpesaCheckout.as_view(), name="checkout"),
    path("callback/", views.MpesaCallBack.as_view(), name="callback"),
]