from django.shortcuts import render
import logging
from django.views import view
from .gateway import MpesaGateWay

gateway = MpesaGateWay()


class MpesaCheckout(view):
    def post(self, request, *args, **kwargs):
        data = request.body

class MpesaCallBack(view):
    pass