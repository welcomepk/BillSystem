from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils.translation import gettext_lazy as _
from .storage import OverwriteStorage
import os


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
    has_membership = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS =  []

    @property
    def get_silver_items(self):
       return self.silver.all()
    
    def is_verified(self):
        return self.profile.is_verified

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

# class Tokens(models.Model):
#     token = models.CharField(max_length = 128, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add = True)

#     class Meta:
#         abstraction = True

#     def __str__(self):
#         return f"{self.user} ({self.token})"

class ForgotPasswordToken(models.Model):
    user = models.OneToOneField(User, related_name="forgot_password_token", on_delete = models.CASCADE)
    token = models.CharField(max_length = 128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return f"{self.user} ({self.token})"


class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, related_name="email_verification_token", on_delete = models.CASCADE)
    token = models.CharField(max_length = 128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return f"{self.user} ({self.token})"


def upload_avatar(instance, file_name):
  
    return os.path.join('avatars', str(instance.user.id), file_name)
    # print("instance in upload file => ", instance.user.id)
    # if instance:
    #     return f"avatars/{file_name}_{instance.user.id}"
    # return f"avatars/{file_name}"


def upload_to(instance, file_name):
    print("instance in upload file => ", instance.user.id)
    if instance:
        return f"avatars/{file_name}_{instance.user.id}"
    return f"avatars/{file_name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    avatar = models.ImageField(_("Avatar"), max_length=300,  storage=OverwriteStorage(), upload_to=upload_avatar, default='avatars/default.png')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"profile : {self.user.email}"