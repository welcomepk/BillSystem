from django.db import models
from account.models import User


class Order(models.Model):
    user = models.OneToOneField(User, related_name = "membership", on_delete=models.CASCADE)
    order_product = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_product


TRIAL = "TRIAL"
PRO = "PRO"


MembershipTypes = (
    (TRIAL, "Trial"),
    (PRO, "Pro"),
)

class Membership(models.Model):
        
    user = models.OneToOneField(User, related_name = "plan", on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=20, choices=MembershipTypes, default=TRIAL)
    membership_amount = models.CharField(max_length=25, default=500)
    membership_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    membership_order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.membership_type}"

