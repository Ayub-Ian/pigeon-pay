import logging
import time
import math
import base64
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
from pigeon.settings import env
from phonenumber_field.phonenumber import PhoneNumber


from .models import Payment

logging = logging.getLogger("default")

class MpesaGateWay:
    shortcode = None
    consumer_key = None
    consumer_secret = None
    access_token_url = None
    access_token = None
    access_token_expiration = None
    checkout_url = None
    timestamp = None


    def __init__(self):
        self.now = datetime.now()
        self.shortcode = env("MPESA_SHORTCODE")
        self.consumer_key = env("MPESA_CONSUMER_KEY")
        self.consumer_secret = env("MPESA_CONSUMER_SECRET")
        self.access_token_url = env("MPESA_ACCESS_TOKEN_URL")

        self.password = self.generate_password()
        self.callback_url = env("MPESA_CALLBACK_URL")
        self.checkout_url = env("MPESA_CHECKOUT_URL")

        try:
            self.access_token = self.getAccessToken()
            if self.access_token is None:
                raise Exception("Request for access token failed.")
        except Exception as e:
            logging.error("Error {}".format(e))
        else:
            self.access_token_expiration = time.time() + 3400

    def getAccessToken(self):
        try:
            res = requests.get(
                self.access_token_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
            )
        except Exception as err:
            logging.error("Error {}".format(err))
            raise err
        else:
            token = res.json()["access_token"]
            self.headers = {"Authorization": "Bearer %s" % token}
            return token

    class Decorators:
        @staticmethod
        def refreshToken(decorated):
            def wrapper(gateway, *args, **kwargs):
                if (
                    gateway.access_token_expiration
                    and time.time() > gateway.access_token_expiration
                ):
                    token = gateway.getAccessToken()
                    gateway.access_token = token
                return decorated(gateway, *args, **kwargs)

            return wrapper


    def generate_password(self):
        """Generates mpesa api password using the provided shortcode and passkey"""
        self.timestamp = self.now.strftime("%Y%m%d%H%M%S")
        password_str = env("MPESA_SHORTCODE") + env("MPESA_PASS_KEY") + self.timestamp
        password_bytes = password_str.encode("ascii")
        return base64.b64encode(password_bytes).decode("utf-8")

    @Decorators.refreshToken
    def stk_push_request(self, payload):
        request = payload["request"]
        data = payload["data"]
        amount = data["amount"]
        phone_number = data["phone_number"]
        req_data = {
            "BusinessShortCode": self.shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": math.ceil(float(amount)),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": "Test",
            "TransactionDesc": "Test",
        }

        res = requests.post(
            self.checkout_url, json=req_data, headers=self.headers, timeout=30
        )
        res_data = res.json()
        logging.info("Mpesa request data {}".format(req_data))
        logging.info("Mpesa response info {}".format(res_data))

        if res.ok:
            data["ip"] = request.META.get("REMOTE_ADDR")
            data["checkout_request_id"] = res_data["CheckoutRequestID"]

            Payment.objects.create(**data)
        return res_data
    
    def check_status(self, data):
        try:
            status = data["Body"]["stkCallback"]["ResultCode"]
        except Exception as e:
            logging.error(f"Error: {e}")
            status = 1
        return status

    def get_payment_object(data):
        checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
        payment, _ = Payment.objects.get_or_create(
            checkout_request_id=checkout_request_id
        )

        return payment

    def handle_successful_pay(self, data, transaction):
        items = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
        for item in items:
            if item["Name"] == "Amount":
                amount = item["Value"]
            elif item["Name"] == "MpesaReceiptNumber":
                receipt_no = item["Value"]
            elif item["Name"] == "PhoneNumber":
                phone_number = item["Value"]

        transaction.amount = amount
        transaction.phone_number = PhoneNumber(raw_input=phone_number)
        transaction.receipt_no = receipt_no
        transaction.confirmed = True

        return transaction

    def callback_handler(self, data):
        status = self.check_status(data)
        payment = self.get_payment_object(data)
        if status==0:
            self.handle_successful_pay(data, payment)
        else:
            payment.status = 1

        payment.status = status
        payment.save()


        logging.info("Transaction completed info {}".format(payment))

        return status