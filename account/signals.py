
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User
from account.models import EmailVerificationToken
from .helpers import send_verification_email
import random

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        token = random.randint(999, 9999)
        if send_verification_email(instance=instance, token=token):
            print("email has not been sent yet")
            EmailVerificationToken.objects.create(user = instance, token = token)