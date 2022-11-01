from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class Address(models.Model):
    state = models.CharField(max_length = 40)
    dist = models.CharField(max_length = 50)
    pincode = models.CharField(max_length = 50)


class User(AbstractUser):
    username = None
    shop_name = models.CharField(max_length = 128)
    email = models.EmailField(unique = True)
    phone_no = models.CharField(max_length = 14)
    state = models.CharField(max_length = 128)
    dist = models.CharField(max_length = 128)
    pincode = models.CharField(max_length = 18, null = True, blank = True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS =  []
