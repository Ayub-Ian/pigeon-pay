from django.http import HttpResponse
from django.shortcuts import render
import logging
from django.views import View
from django.views.generic.edit import FormView
from .forms import MpesaSTKForm
from .gateway import MpesaGateWay

gateway = MpesaGateWay()


class MpesaCheckout(FormView):
    form_class = MpesaSTKForm
    success_url = "payment:callback"

    def form_valid(self, form) -> HttpResponse:
        self.amount = form.cleaned_data['amount']
        self.phone_number = form.cleaned_data['phone_number']
        if form.is_valid():
            data = {"phone_number": self.phone_number, "amount": self.amount}
            payload = {"data": data, "request": self.request}
            res = gateway.stk_push_request(payload)
        return super().form_valid(form)


class MpesaCallBack(View):
    pass