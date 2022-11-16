from django.db import models
from account.models import User, Customer
from django.utils import timezone
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this

class PurchasedBy(models.Model):
    user = models.ForeignKey(User, related_name = 'purchases',on_delete=models.CASCADE)
    seller_name = models.CharField(max_length = 128)
    total_amount = models.FloatField()  
    paid_amount = models.FloatField()  
    gst = models.FloatField()
    golditems = models.JSONField(default = '{}')
    silveritems = models.JSONField(default = '{}')
    # purchased_date = models.DateField(auto_now_add = True, blank = True, null = True)
    timestamp = models.DateTimeField(auto_now_add = True)
    created_at = models.DateField()

    def __str__(self):
        return f"{self.id} => {self.user.first_name} {self.created_at}"

class Gold(models.Model):
    parchased_by = models.ForeignKey(
        PurchasedBy,
        related_name='gold_items',
        on_delete=models.CASCADE,
        blank = True,
        null = True
    )
    shop = models.ForeignKey(
        User, 
        related_name = 'gold_items',
        on_delete=models.CASCADE
    )
    item_name = models.CharField(max_length = 128)
    item_type = models.CharField(max_length=20, default='gold')

    karet = models.IntegerField()
    gross_wt = models.FloatField( blank = True, null = True)
    net_wt = models.FloatField( blank = True, null = True)
    grm_wt = models.FloatField( blank = True, null = True)
    stone_wt = models.FloatField( blank = True, null = True)
    fine_wt = models.FloatField( blank = True, null = True)
    price = models.FloatField()
    qty = models.IntegerField()

    def __str__(self):
        return f"shop {self.shop} {self.item_name}"

class Silver(models.Model):
    parchased_by = models.ForeignKey(
        PurchasedBy,
        related_name='silver_items',
        on_delete=models.CASCADE,
        blank = True,
        null = True
    )
    shop = models.ForeignKey(
        User, 
        related_name = 'silver_items',
        on_delete=models.CASCADE
    )
    item_name = models.CharField(max_length = 128)
    item_type = models.CharField(max_length=20, default='silver')
    gross_wt = models.FloatField( blank = True, null = True)
    net_wt = models.FloatField( blank = True, null = True)
    grm_wt = models.FloatField( blank = True, null = True)
    stone_wt = models.FloatField( blank = True, null = True)
    fine_wt = models.FloatField( blank = True, null = True)
    price = models.FloatField()
    qty = models.IntegerField()
    
    def __str__(self):
        return f"shop {self.shop} {self.item_name}"

class Sell(models.Model):
    shop = models.ForeignKey(User, related_name = 'sells', on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer,   related_name='buys', on_delete = models.CASCADE)
    customer_name = models.CharField(max_length=128)
    gold_items = models.JSONField(default = '{}')
    silver_items = models.JSONField(default = '{}')
    total_amount = models.FloatField()
    paid_amount = models.FloatField()
    gst = models.FloatField()
    created_at = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"from {self.shop} to {self.customer.full_name}"

class GoldSilverRate(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "goldsilverrates")
    gold_price = models.FloatField(default = 0.0)
    silver_price = models.FloatField(default = 0.0)

    def __str__(self):
        return f"{self.user} => G-{self.gold_price}  S-{self.silver_price}"

    @receiver(post_save, sender=User) #add this
    def create_user_rates(sender, instance, created, **kwargs):

        if created:
            GoldSilverRate.objects.create(user=instance)

# class SellHistory(models.Model):
#     shop_name = models.CharField(max_length = 128)
#     customer_name = models.CharField(max_length = 128)
#     timestamp = models.DateTimeField(auto_now = True)

class DateDemo(models.Model):
    date = models.DateField()
    datetime = models.DateTimeField(auto_now=True)
