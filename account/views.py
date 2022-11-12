from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .serializer import UserSerializer, RegisterSerializer
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['GET'])
def is_exists(request):
    email = request.GET.get("email")
    try:
        user = User.objects.get(email = email)
        print(user)
        return Response({"msg" : "user already exists with this email address"})
    except User.DoesNotExist:
        return Response({"error" : "user does not exists"}, status=status.HTTP_400_BAD_REQUEST)
    return Response("good to go with verify user")

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
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


# class SignUpView(generics.CreateAPIView):
#   permission_classes = (AllowAny,)
#   serializer_class = RegisterSerializer