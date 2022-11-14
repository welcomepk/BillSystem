from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .serializers import UserSerializer, RegisterSerializer, RequestPaswordResetEmailSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view
from .helpers import send_forget_password_mail

def check_user_exists(email):
    if User.objects.filter(email = email).exists():
        return True
    return False

@api_view(['GET'])
def is_exists(request):
    email = request.GET.get("email")
    if check_user_exists(email):
        return Response({"msg" : "user already exists with this email address"})
    return Response({"error" : "user does not exists"}, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['payload'] = {
            "profile" : {
                "email" : user.email,
                "shop_name" : user.shop_name,
                "phone_no" : user.phone_no,
            },
            "gold_price" : user.goldsilverrate.gold_price,
            "silver_price" : user.goldsilverrate.gold_price,

        }
        # ...

        return token



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class SignUpView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "msg" : "User is created"
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPaswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPaswordResetEmailSerializer

    def post(self, request):
        print("user id ", request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        status = send_forget_password_mail("kamblepk020@gmail.com")
        if status:
            return Response(f'Good to go {email} successfully sent')
        else:
            return Response({"error" : "mail can not be sent"}, status=status.HTTP_400_BAD_REQUEST)
            

        
# class SignUpView(generics.CreateAPIView):
#   permission_classes = (AllowAny,)
#   serializer_class = RegisterSerializer