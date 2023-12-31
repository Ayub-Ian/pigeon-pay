from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
verify = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID)

def send_notification(phone):
    verify.verifications.create(to=phone, channel='sms')


def verify_otp(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
    except TwilioRestException as e:
        print("Twilio Error: {}".format(e))
        return False
    return result.status == 'approved'

