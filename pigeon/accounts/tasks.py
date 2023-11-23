from celery import shared_task
from .verify import send_notification

@shared_task
def send_phone_verification(phone):
    send_notification(phone)