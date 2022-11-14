from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class Address(models.Model):
    state = models.CharField(max_length = 40)
    dist = models.CharField(max_length = 50)
    pincode = models.CharField(max_length = 50)

USER_TYPE = (
     ("retailer", "retailer"),
    ("dealer", "dealer"),
    ("customer", "customer"),
)

class User(AbstractUser):
    username = None
    shop_name = models.CharField(max_length = 128)
    user_type = models.CharField(max_length=9,
                  choices=USER_TYPE,
                  default="retailer")
    # user_type = models.CharField(max_length = 128, default="retailer")
    email = models.EmailField(unique = True)
    phone_no = models.CharField(max_length = 14)
    state = models.CharField(max_length = 128)
    dist = models.CharField(max_length = 128)
    address = models.CharField(max_length = 128)
    pincode = models.CharField(max_length = 18, null = True, blank = True)
    adhaar_no = models.CharField(max_length = 128, unique = True)
    pan_no = models.CharField(max_length = 20, unique = True)
    gst_no = models.CharField(max_length = 20, unique = True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS =  []

    @property
    def get_silver_items(self):
       return self.silver.all()


class Customer(models.Model):
    
    shop = models.ForeignKey(User, related_name = "customers", on_delete=models.CASCADE)
    full_name = models.CharField(max_length = 128)
    email = models.EmailField(unique = True)
    phone_no = models.CharField(max_length = 14)
    state = models.CharField(max_length = 128)
    dist = models.CharField(max_length = 128)
    address = models.CharField(max_length = 128)
    adhaar_no = models.CharField(max_length = 128, unique = True)
    pan_no = models.CharField(max_length = 20, unique = True)
    gst_no = models.CharField(max_length = 20, unique = True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class ForgotPasswordToken(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    token = models.CharField(max_length = 128)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user} ({self.token})"

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete = models.CASCADE)
#     avatar = 

