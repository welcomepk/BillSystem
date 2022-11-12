from django.db import models
from account.models import User, Customer


class PurchasedBy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_name = models.CharField(max_length = 128)
    total_amount = models.FloatField()  
    paid_amount = models.FloatField()  
    gst = models.FloatField()
    purchased_date = models.DateField(auto_now_add = True, blank = True, null = True)

    def __str__(self):
        return f"{self.id} => {self.user.first_name} {self.purchased_date}"



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
    customer = models.ForeignKey(Customer,   related_name='sells', on_delete = models.CASCADE)
