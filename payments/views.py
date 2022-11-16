import json
import environ
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from .models import Order, Membership
from .serializers import OrderSerializer, MembershipSerializer
from datetime import datetime, date, timedelta

env = environ.Env()

# you have to create .env file in same folder where you are using environ.Env()
# reading .env file which located in api folder
environ.Env.read_env()


@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    # amount = request.data['amount']
    # name = request.data['name']

    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    payment = client.order.create({"amount": 500 * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function
    try:
        user = User.objects.get(id = request.user.id)
        # user = User.objects.get(id = 8)
    except User.DoesNotExist:
        return Response({"error" : "User does not exists"}, status=status.HTTP_400_BAD_REQUEST)

    membership = None
    try:
        membership = Membership.objects.get(user = user)
        # membership.membership_type = 'PRO'
        # membership.membership_amount = amount
        membership.membership_payment_id = payment['id']
        membership.save()
    except Membership.DoesNotExist:
        membership = Membership.objects.get_or_create(user = user,
                                    # order_product=name, 
                                    # membership_amount=amount, 
                                    membership_payment_id=payment['id'])

    serializer = MembershipSerializer(membership)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)


@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend

    res = json.loads(request.data["response"])

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """
    
    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Membership.objects.get(membership_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    try:
        check = client.utility.verify_payment_signature(data)
        today = date.today()
        if check:
            order.isPaid = True
            order.membership_type = 'PRO'
            order.membership_order_date = date.today()
            
            if not order.isNew:
                if today < order.membership_terminate_date: 
                    order.membership_terminate_date = order.membership_terminate_date + timedelta(weeks=1)
                else:
                    order.membership_terminate_date = order.membership_order_date + timedelta(weeks=1)
            else:
                order.isNew = False
                order.membership_terminate_date = order.membership_order_date + timedelta(weeks=1)

            order.save()
            res_data = {
                'message': 'Payment Successfull.'
            }
            return Response(res_data)
        else:
            return Response({"error" : "Payment Failed"}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        print("Unexpected error:", e)
        return Response({'error': 'Something went wrong'}, status=status.HTTP_403_FORBIDDEN)
