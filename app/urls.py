from django.urls import path
from .views import *


urlpatterns = [
    path('sell/', SellingApiView.as_view(), name='sell_product'),
    path('sell/invoice/', SellInvoiceApiView.as_view(), name="sell-invoice"),

    path('purchase/', PurchaseProductApiView.as_view(), name='purchase_product'),
    path('purchase/invoice/', PurchaseInvoiceApiView.as_view(), name="purchase-invoice"),

    path('customers/', CustomersApiView.as_view(), name="customers"),
    path('customers/<int:pk>/', CustomersApiView.as_view(), name="customer_details"),
    path('customers/search/', CustomerSearchApiView.as_view(), name="customer_serach"),
    
    path('products/', ProductsApiView.as_view(), name="available_products"),
    path('products/<int:pk>/', ProductsApiView.as_view(), name="product_details"),
    path('products/search/', ProductSearchApiView.as_view(), name="product_serach"),

    path('gold-silver-price/', GoldSilverRateApiView.as_view(), name='gold-silver-prices'),
]