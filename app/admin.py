from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Gold)
admin.site.register(Silver)
admin.site.register(PurchasedBy)
admin.site.register(Sell)
admin.site.register(GoldSilverRate)
