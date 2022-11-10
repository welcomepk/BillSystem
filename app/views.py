from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GoldSerializer, InvoiceSerializer, SilverSerializer, PurchasedBySerializer
from account.serializer import CustomerSerializer
from .models import Gold, Silver, PurchasedBy
from account.models import User, Customer

class SellingApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(request.data)


class PurchaseProductApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        gold_items = request.data.get('gold')
        silver_items = request.data.get('silver')
        print(request.data)
        gold_serializer = None
        selver_serializer = None
        purchased_by = None
        purchased_data = {
            'user' : request.user.id,
            'seller_name': request.data.get('seller_name'),
            'total_amount': request.data.get('total_amount'),
            'gst': request.data.get('gst'),
            'paid_amount': request.data.get('paid_amount'),
        }
        
        purchased_serializer = PurchasedBySerializer(data=purchased_data)

        if purchased_serializer.is_valid():
            purchased_by = purchased_serializer.save();
           
            data = gold_items[0]
            data['parchased_by'] = purchased_by.id
            
            tobe_saved_golds = []
            tobe_saved_silvers = []
            # User.objects.bulk_create(users)
            if gold_items:
                for gold_item in gold_items:
                    gold_item['parchased_by'] = purchased_by.id
                    gold_serializer = GoldSerializer(data=gold_item)
                    if gold_serializer.is_valid():
                        tobe_saved_golds.append(gold_serializer)
                    else:
                        return Response(gold_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                for save_gold in tobe_saved_golds:
                    save_gold.save()

            if silver_items:
                for silver_item in silver_items:
                    silver_item['parchased_by'] = purchased_by.id
                    silver_serializer = SilverSerializer(data=silver_item)
                    if silver_serializer.is_valid():
                        tobe_saved_silvers.append(silver_serializer)
                    else:
                        return Response(silver_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                for save_silver in tobe_saved_silvers:
                    save_silver.save()

            return Response(purchased_serializer.data)

        else:
            return Response(purchased_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('good to go')



class InvoiceApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format = None):

        invice_no = request.data.get('invice_no')
        if invice_no:
            try:
                purchase_user = PurchasedBy.objects.get(id = invice_no)
                return Response(InvoiceSerializer(purchase_user).data)
            except PurchasedBy.DoesNotExist:
                return Response({"error": "Invalid invice no"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error' : "unknown error"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('plz provide invice_no', status=status.HTTP_400_BAD_REQUEST)


class CustomersApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format = None):
        if pk is not None:
            try:
                customer = Customer.objects.get(id = pk)
                return Response(CustomerSerializer(customer).data)
            except Customer.DoesNotExist:
                return Response({"error": "customer does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            shop = User.objects.get(id = request.user.id)
            customers = Customer.objects.filter(shop = shop)
        except User.DoesNotExist:
            return Response({"error": "shop user does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error' : "unknown error in CustomerApiView"}, status=status.HTTP_400_BAD_REQUEST)

        customers_serializer = CustomerSerializer(customers, many=True)
        return Response(customers_serializer.data)
       
    def post(self, request):

        request.data['shop'] = request.user.id
        customer_serializer = CustomerSerializer(data=request.data)
        if customer_serializer.is_valid():
            customer_serializer.save()
            return Response(customer_serializer.data)
        else:
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format = None):
        try:
            customer = Customer.objects.get(id = pk)
            serializer = CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save();
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
                return Response({"error": "Customer does not exists"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format = None):
        try:
            customer = Customer.objects.get(id = pk)
            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save();
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
                return Response({"error": "Customer does not exists"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = True):
        try:
            customer = Customer.objects.get(id = pk)
            customer.delete()
            return Response({"msg" : "customer deleted successfully"})
        except Customer.DoesNotExist:
            return Response({"error": "Customer does not exists"}, status=status.HTTP_400_BAD_REQUEST)


class CustomerSearchApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format = None):
        
        print(request.user.id)
        q = request.GET.get('search', None)
        try:
            shop = User.objects.get(id = request.user.id)
            customers = Customer.objects.filter(shop = shop)
            print("q =>", q, customers)
            if q:
                customers = customers.filter(Q(full_name__icontains=q) & Q(email__icontains=q))
                customers_serializer = CustomerSerializer(customers, many=True)
            else:
                customers_serializer = CustomerSerializer(customers, many=True)
            return Response(customers_serializer.data)
        except User.DoesNotExist:
            return Response({"error": "shop user does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error' : "unknown error in CustomerSearchApiView"}, status=status.HTTP_400_BAD_REQUEST)
