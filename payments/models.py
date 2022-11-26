from django.db import models
from account.models import User
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this
from datetime import date, datetime, timedelta

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
NONE = "NONE"

MembershipTypes = (
    (TRIAL, "Trial"),
    (PRO, "Pro"),
    (NONE, "None"),
)

class Membership(models.Model):
        
    user = models.OneToOneField(User, related_name = "plan", on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=20, choices=MembershipTypes, default=TRIAL)
    membership_amount = models.CharField(max_length=25, default=500)
    membership_payment_id = models.CharField(max_length=100, null = True, blank=True)
    isPaid = models.BooleanField(default=False)
    isNew = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    membership_order_date = models.DateField(null=True, blank=True)
    membership_terminate_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.membership_type}"

    # def save(self, *args, **kwargs): 

    #     today = date.today()
    #     if self.isPaid and self.isNew:
    #         # self.terminate_date = self.order_date + timedelta(days=2)
    #         self.membership_terminate_date = self.membership_order_date + timedelta(weeks=1)
    #         self.isNew = False

    #     elif self.isPaid and not self.isNew:
    #         if today < self.membership_terminate_date: 
    #             self.membership_terminate_date = self.membership_order_date + timedelta(weeks=1) + (self.membership_terminate_date - today)
    #         else:
    #             self.membership_terminate_date = self.membership_order_date + timedelta(weeks=1)
    #     super(Membership, self).save(*args, **kwargs)       

    def has_membership(self):
        today = date.today()
        if self.membership_terminate_date and self.membership_order_date:
            return today < self.membership_terminate_date and self.isPaid 
        return False


    @receiver(post_save, sender=User) #add this
    def create_membership(sender, instance, created, **kwargs):
        if created:
            Membership.objects.create(user=instance)