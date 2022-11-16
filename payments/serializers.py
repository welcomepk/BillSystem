from rest_framework import serializers

from .models import Order, Membership

class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = Order
        fields = '__all__'
        depth = 2


class MembershipSerializer(serializers.ModelSerializer):
    # membership_order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")
    # membership_terminate_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = Membership
        fields = '__all__'
        # exclude = ('membership_order_date', 'membership_terminate_date')
        depth = 2