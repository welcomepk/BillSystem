from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
import smtplib
from django.conf import settings

def send_forget_password_mail(email = None, token = None):

    # Note : aws http://52.66.199.187/api/account/forgot-password/
    # Note : localhost http://localhost:8000/api/account/forgot-password/{token}/
    subject = "Forget Password Link (BY .LTD)"
    message = f"Hello, click on the link to reset password http://52.66.199.187/api/account/forgot-password/{token}/" #aws
    # message = f"Hello, click on the link to reset password http://localhost:8000/api/account/forgot-password/{token}/" #localhost
    from_email = settings.EMAIL_HOST_USER
    email_password = settings.EMAIL_HOST_PASSWORD
    recipient_list = [email]
    print(from_email, email_password)
    try:
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)  
    except smtplib.SMTPServerDisconnected:
        return False
    except:
        return False
    return True


def send_verification_email(instance, token):
    subject = "Forget Password Link (BY .LTD)"
    message = f"Hello {instance.first_name}, use this Token {token} to verify your mail"
    from_email = settings.EMAIL_HOST_USER
    email_password = settings.EMAIL_HOST_PASSWORD
    recipient_list = [instance.email]
    print(from_email, email_password)
    try:
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)  
    except smtplib.SMTPServerDisconnected:
        return False
    except:
        return False
    return True


def is_user_verified(user):
    return user.profile.is_verified