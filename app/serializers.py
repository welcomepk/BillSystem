from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Gold, Silver, PurchasedBy
from account.serializer import UserSerializer

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
            'gold_items',
            'silver_items',
           )