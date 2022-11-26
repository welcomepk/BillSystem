from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def getRoutes(request):
    print(request.method)
    import os
    
    routes = [
        '/api/account/login/',
        '/api/account/login/refresh/',
        '/api/app/sell/',
        '/api/app/purchase/',
        {'server_type' : os.environ.get('DJANGO_SETTINGS_MODULE')}
    ]
    return Response(routes)

urlpatterns = [

    # getting all api routes
    path('', getRoutes, name= 'api_routes'),

    # account app (signup, login)
    path('account/', include('account.urls')),

    # main app
    path('app/', include('app.urls')),

    # payments
    path('razorpay/', include("payments.urls")),

    # tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]