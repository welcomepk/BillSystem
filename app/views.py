from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GoldSerializer, InvoiceSerializer, SilverSerializer, PurchasedBySerializer
from account.serializer import CustomerSerializer
from .models import Gold, Silver, PurchasedBy
from account.models import User, Customer
from django.db.models.lookups import GreaterThan, LessThan
from django.db.models import F, Q, When



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
                    gold_item['shop'] = request.user.id
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
                    silver_item['shop'] = request.user.id
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


# Note: invice_no => purchsed_by id(acts as invice_no)
class InvoiceApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format = None):

        invice_no = request.GET.get('invice_no')
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
                customers = customers.filter(Q(full_name__icontains=q) | Q(email__icontains=q))
                customers_serializer = CustomerSerializer(customers, many=True)
            else:
                customers_serializer = CustomerSerializer(customers, many=True)
            return Response(customers_serializer.data)
        except User.DoesNotExist:
            return Response({"error": "shop user does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error' : "unknown error in CustomerSearchApiView"}, status=status.HTTP_400_BAD_REQUEST)


class ProductsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format = None):
        
        user = User.objects.get(id = request.user.id)

        if pk is not None:
            item_type = request.GET.get('type')
            try:
                item = None
                if item_type.lower() == 'silver':
                    item = Silver.objects.get(id = pk)
                    return Response(SilverSerializer(item).data)
                else:
                    item = Gold.objects.get(id = pk)
                    return Response(GoldSerializer(item).data)

            except Silver.DoesNotExist:
                return Response({"error": "This silver item does not exists"}, status=status.HTTP_400_BAD_REQUEST)
            except Gold.DoesNotExist:
                return Response({"error": "This gild item does not exists"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error' : "unknown error while getting product details"}, status=status.HTTP_400_BAD_REQUEST)
            

        gold_items = user.gold_items.all()
        silver_items = user.silver_items.all()
        gold_serializer = GoldSerializer(gold_items, many = True)
        silver_serializer = SilverSerializer(silver_items, many = True)
        
        products = {
            "gold_items" : gold_serializer.data,
            "silver_items" : silver_serializer.data
        }
        return Response(products)

    def post(self, request, format = None):
    
        gold_items = request.data.get('gold_items')
        silver_items = request.data.get('silver_items')
        
        if not gold_items or not silver_items:
            return Response({"error" : "No items were provided"}, status=status.HTTP_400_BAD_REQUEST)

        gold_serializer = None
        silver_serializer = None
        tobe_saved_golds = []
        tobe_saved_silvers = []

        # User.objects.bulk_create(users)
        if gold_items:
            for gold_item in gold_items:
                # gold_item['parchased_by'] = purchased_by.id
                gold_item['shop'] = request.user.id
                gold_serializer = GoldSerializer(data=gold_item)
                if gold_serializer.is_valid():
                    tobe_saved_golds.append(gold_serializer)
                else:
                    return Response(gold_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            for save_gold in tobe_saved_golds:
                save_gold.save()

        if silver_items:
            for silver_item in silver_items:
                # silver_item['parchased_by'] = purchased_by.id
                silver_item['shop'] = request.user.id
                silver_serializer = SilverSerializer(data=silver_item)
                if silver_serializer.is_valid():
                    tobe_saved_silvers.append(silver_serializer)
                else:
                    return Response(silver_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            for save_silver in tobe_saved_silvers:
                save_silver.save()
            
        return Response({"msg" : "items are saved successfully"}, status=status.HTTP_201_CREATED)

    def patch(self, request, pk, format = None):
        item_type = request.GET.get('type')
        try:
            if item_type.lower() == "silver":
                silver_item = Silver.objects.get(id = pk)
                serializer = SilverSerializer(silver_item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save();
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                gold_item = Gold.objects.get(id = pk)
                serializer = GoldSerializer(gold_item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save();
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Silver.DoesNotExist:
                return Response({"error": "silver item does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        except Gold.DoesNotExist:
            return Response({"error": "gold item does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "unkwon error while updating product"}, status=status.HTTP_400_BAD_REQUEST)


    # def delete(self, request, pk = None, format = None):

    #     item_type = request.GET.get('type')
    #     try:
    #         item = None
    #         if item_type == 'silver':
    #             item = Silver.objects.get(id = pk)
    #         else:
    #             item = Gold.objects.get(id = pk)
    #         item.delete()
    #         return Response({"msg" : "item deleted successfully"})
    #     except Silver.DoesNotExist:
    #         return Response({"error": "This silver item does not exists"}, status=status.HTTP_400_BAD_REQUEST)
    #     except Gold.DoesNotExist:
    #         return Response({"error": "This gild item does not exists"}, status=status.HTTP_400_BAD_REQUEST)
    #     except:
    #         return Response({'error' : "unknown error while getting product details"}, status=status.HTTP_400_BAD_REQUEST)
            
class ProductSearchApiView(APIView):

    def get(self, request, format = None):
    
        q = request.GET.get('search', None)
        item_type = request.GET.get("item_type").lower()
        try:
            user = User.objects.get(id = request.user.id)
            gold_items = [gold_item for gold_item in user.gold_items.filter(Q(item_name__icontains=q)) if gold_item.qty > 0]
            silver_items = [silver_item for silver_item in user.silver_items.filter(Q(item_name__icontains=q)) if silver_item.qty > 0]
            
            print("gold items ===> ", gold_items)

            if q:
                
                # gold_products = gold_items.filter(Q(item_name__icontains=q) & Q(price__icontains=q))
                gold_serializer = GoldSerializer(gold_items, many = True)
                # silver_products = silver_items.filter(Q(item_name__icontains=q) & Q(price__icontains=q))
                silver_serializer = SilverSerializer(silver_items, many = True)

                if item_type == 'gold':
                    return Response({"gold_items" : gold_serializer.data})
                elif item_type == 'silver':
                    return Response({"silver_items" : silver_serializer.data})
                
                
                products = {
                    "gold_items" : gold_serializer.data,
                    "silver_items" : silver_serializer.data
                }
                return Response(products)

            else:
               
                gold_serializer = GoldSerializer(gold_items, many = True)
                silver_serializer = SilverSerializer(silver_items, many = True)
                
                products = {
                    "gold_items" : [],
                    "silver_items" : []
                }
                return Response(products)
            return Response({"msg" : f"{q} {item_type}"})
        except User.DoesNotExist:
            return Response({"error" : "User does not exists"}, status=status.HTTP_400_BAD_REQUEST)


class SellingApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            shop = User.objects.get(id = request.user.id)
            customer = shop.customers.get(id = request.data.get("shop"))

            gold_items = request.data.get("gold_items")
            silver_items = request.data.get("silver_items")
            
            for gold_item in gold_items:
                try:
                    gold = shop.gold_items.get(id = gold_item.get('id'))
                    if int(gold_item['qty']) > gold.qty:
                        return Response({"error" : f"quantity({gold_item['qty']}) is larger than available stocks in GOLD items for id={gold_item.get('id')}"}, status=status.HTTP_400_BAD_REQUEST)
                except Gold.DoesNotExist:
                    return Response({"error" : f"Gold item not found with this id({gold_item.get('id')})"}, status=status.HTTP_400_BAD_REQUEST)
        
            for silver_item in silver_items:
                try:
                    silver = shop.silver_items.get(id = silver_item.get('id'))
                    if int(silver_item['qty']) > silver.qty:
                        return Response({"error" : f"quantity({silver_item['qty']}) is larger than available stocks in SILVER items for id={silver_item.get('id')}"}, status=status.HTTP_400_BAD_REQUEST)
                except Silver.DoesNotExist:
                    return Response({"error" : f"Silver item not found with this id({silver_item.get('id')})"}, status=status.HTTP_400_BAD_REQUEST)

            # next save all minus qty and save items
            # create Serializer for Selling
            # varify serializer at start of the code ()
            # save serializer if valid
            
            selling_serializer = None

        except Silver.DoesNotExist:
            return Response({"error" : "Does not found this silver item"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error" : "This buisness account is not active or exists."}, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({"error" : "Customer does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(request.data)