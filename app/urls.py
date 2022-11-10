from django.urls import path
from .views import SellingApiView, PurchaseProductApiView, InvoiceApiView, CustomersApiView, CustomerSearchApiView


urlpatterns = [
    path('sell/', SellingApiView.as_view(), name='sell_product'),
    path('purchase/', PurchaseProductApiView.as_view(), name='purchase_product'),
    path('invoice/', InvoiceApiView.as_view(), name="invoice"),
    path('customers/', CustomersApiView.as_view(), name="customers"),
    path('customers/<int:pk>/', CustomersApiView.as_view(), name="customer_details"),
    path('customers/search/', CustomerSearchApiView.as_view(), name="customer_serach"),
]