from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Gold, Silver, PurchasedBy, Sell, GoldSilverRate
from account.serializers import UserSerializer


class GoldSilverRateSerializer(ModelSerializer):

    class Meta:
        model = GoldSilverRate
        fields = ('gold_price', 'silver_price')

class GoldItemDescSerializer(serializers.Serializer):
    item_name = serializers.CharField(max_length = 128)
    karet = serializers.IntegerField()
    gross_wt = serializers.FloatField()
    net_wt = serializers.FloatField()
    grm_wt = serializers.FloatField()
    stone_wt = serializers.FloatField()
    fine_wt = serializers.FloatField()
    price = serializers.FloatField()
    qty = serializers.IntegerField()

    class Meta:
        fields = '__all__'


class SilverItemDescSerializer(serializers.Serializer):
    item_name = serializers.CharField(max_length = 128)
    gross_wt = serializers.FloatField()
    net_wt = serializers.FloatField()
    grm_wt = serializers.FloatField()
    stone_wt = serializers.FloatField()
    fine_wt = serializers.FloatField()
    price = serializers.FloatField()
    qty = serializers.IntegerField()

    class Meta:
        fields = '__all__'


class GoldSerializer(ModelSerializer):

    class Meta:
        model = Gold
        fields = '__all__'

class SilverSerializer(ModelSerializer):
    class Meta:
        model = Silver
        fields = '__all__'


class PurchasedBySerializer(ModelSerializer):

    class Meta:
        model = PurchasedBy
        fields = '__all__'


    
class InvoiceSerializer(ModelSerializer):
  gold_items = GoldSerializer(many=True, read_only=True)
  silver_items = SilverSerializer(many=True, read_only=True)
  
  class Meta:
        model = PurchasedBy
        fields = (
            'user',
            'total_amount',
            'paid_amount',
            'created_at',
            'gold_items',
            'silver_items',
           )


# class SellInvoiceSerializer(ModelSerializer):
#   gold_items = GoldSerializer(many=True, read_only=True)
#   silver_items = SilverSerializer(many=True, read_only=True)
  
#   class Meta:
#         model = Sell
#         fields = (
#             'user',
#             'total_amount',
#             'gold_items',
#             'silver_items',
#            )


class SellingSerializer(ModelSerializer):
    class Meta:
        model = Sell
        fields = "__all__"

class SellInvoiceSerializer(ModelSerializer):

    class Meta:
        model = Sell
        exclude = ['gold_items', 'silver_items']


# class ProductsSerializer(ModelSerializer):  
#   gold_items = GoldSerializer(many=True, read_only=True)
#   silver_items = SilverSerializer(many=True, read_only=True)
#   class Meta:
#     model = 

