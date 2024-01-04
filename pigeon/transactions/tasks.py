from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def send_confirmation_email(transaction, sender_name, sender_email, recepient_mail, recepient_name):

    base_url = "http://127.0.0.1:8000"
    path = transaction['shareable_url'] 

    concatenated_url = base_url + path


    context = {
        'sender_name': sender_name,
        'sender_email': sender_email,
        'recepient_name': recepient_name,
        'transaction_title' : transaction['title'],
        'transaction_amount' : transaction['amount'],
        'initiator_role' : transaction['role'],
        'transaction_no': transaction['reference_no'],
        'transaction_link': concatenated_url

    }

    html_message = render_to_string("transactions/email/agreement_email.html", context=context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
       subject = 'Accept Escrow Agreement', 
       body = plain_message,
       from_email = None ,
       to= [recepient_mail]
        )

    message.attach_alternative(html_message, "text/html")
    message.send()