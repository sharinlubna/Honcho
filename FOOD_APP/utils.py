#additional utilities

from django.core.mail import send_mail
from django.conf import settings

def send_email_to_client():
    subject = "Order Placed"
    message = "Test message"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["7427user@gmail.com"]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)