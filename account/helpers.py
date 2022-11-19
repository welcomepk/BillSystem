from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site

import smtplib
from django.conf import settings

def send_forget_password_mail(email = None, token = None):

    
    subject = "Forget Password Link (BY .LTD)"
    message = f"Hello, click on the link to reset password http://localhost:8000/api/account/forgot-password/{token}/"
    from_email = settings.EMAIL_HOST_USER
    email_password = settings.EMAIL_HOST_PASSWORD
    recipient_list = [email]
    try:
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)  
    except smtplib.SMTPServerDisconnected:
        return False
    except:
        return False
    return True