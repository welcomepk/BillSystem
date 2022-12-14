from django.shortcuts import render, redirect
from .models import User, ForgotPasswordToken, EmailVerificationToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .serializers import UserSerializer, RegisterSerializer, RequestPaswordResetEmailSerializer, MembershipSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from .helpers import send_forget_password_mail, is_user_verified
from app.models import GoldSilverRate
import uuid


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def has_membership(request):    
    user_membership = request.user.plan
    serializer = MembershipSerializer(user_membership)
    if request.user.has_membership:
        if not user_membership.has_membership():
            user_membership.membership_type = 'NONE'
            user_membership.save()
            request.user.has_membership = False
            request.user.is_active = False
            request.user.save()
            return Response({'has_membership': False, 'details' : serializer.data})
        return Response({'has_membership': True, 'details' : serializer.data})
    else:
        return Response({'has_membership': False, 'details' : serializer.data})
    return Response("good to go") 


class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format = None):
        try:
            user = request.user
            if user.plan.has_membership():
                user.has_membership = True
                user.plan.membership_type = "PRO"
                user.plan.save()
                user.save()
                print(f"{user} has membership")
            else:
                user.has_membership = False
                user.plan.membership_type = "NONE"
                user.plan.save()
                user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error" : "user does not exists or invalid id"}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format = None):
        try:
            user = User.objects.get(id = pk)
            serializer = UserSerializer(user, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error" : "user does not exists or invalid id"}, status=status.HTTP_400_BAD_REQUEST)
    

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

        gold_price = ''
        silver_price = ''
        
        if GoldSilverRate.objects.filter(user = user).exists():
           gold_price = user.goldsilverrates.gold_price
           silver_price =  user.goldsilverrates.gold_price
        # Add custom claims
        token['payload'] = {
            "profile" : {
                "email" : user.email,
                "shop_name" : user.shop_name,
                "phone_no" : user.phone_no,
                "has_membership" : user.has_membership,
            },
            "gold_price" : gold_price,
            "silver_price" : silver_price,
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


def change_password_success(request, name):
        return render(request, 'change-password-success.html', context={"name" : name})

def change_password_confirm(request, token):
    context = {}
    error = None
    if request.method == 'POST':
        try:
            user_token = ForgotPasswordToken.objects.get(token = token)
            user = user_token.user
            password = request.POST.get('password', None)
            re_password = request.POST.get('re-password', None)
            if password and re_password:
                if password == re_password:
                    user.set_password(password)
                    user.save()
                    user_token.delete()
                    return redirect('forgot-password-success', name = user.first_name)
                else:
                    error = "Both password fields should match"
            else:
                error = "Both fiels are required"
            context = {
                "error" : error
            }
            return render(request, 'change-password.html', context=context)
            
        except ForgotPasswordToken.DoesNotExist:
            return render(request, 'invalid-token.html')

    return render(request, 'change-password.html')

    context = {}
    if request.method == "POST":
        error = "Both password fields should match"
        password = request.POST.get('password')
        re_password = request.POST.get('re-password')
        print(password, re_password)
        context = {
           "password" : password
        }
    return render(request, 'change-password.html', context=context)
    

class RequestPaswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPaswordResetEmailSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = str(uuid.uuid4())
        email = request.data.get('email')
        try:
            user = User.objects.get(email = email)
            if not is_user_verified(user):

                return Response({
                            "detail": "User is not verified",
                            "code": "user_not_verified"
                        }, status=status.HTTP_400_BAD_REQUEST)

            forgot_password_token, created = ForgotPasswordToken.objects.get_or_create(user = user)
            forgot_password_token.token = token
            forgot_password_token.save()
            mail_status = send_forget_password_mail(email=email, token = token)
            if mail_status:
                return Response(f'Good to go {email} successfully sent')
            else:
                return Response({"error" : "mail can not be sent"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:   
            return Response({'error' : "User does not exists with this email"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "unkown error at RequestPaswordResetEmail"}, status=status.HTTP_400_BAD_REQUEST)


# class SignUpView(generics.CreateAPIView):
#   permission_classes = (AllowAny,)
#   serializer_class = RegisterSerializer


@api_view(['POST'])
def send_verification_email(request):

    # token = random.randint(999, 9999)
    # if send_verification_email(instance=instance, token=token):
    #     print("email has not been sent yet")
    #     EmailVerificationToken.objects.create(user = request.user, token = token)
    return Response(f"{request.data}")

@api_view(['POST'])
def verify_email(request):
    token = request.data.get('token', None)
    email = request.data.get('email', None)
    if token and email:
        try:
            token_to_check = EmailVerificationToken.objects.get(token = token)

            if token_to_check.user.email == email:
                token_to_check.user.profile.is_verified = True
                token_to_check.user.profile.save()
                token_to_check.delete()
                return Response(f"{token_to_check.user.email} is verified successfully")
            return Response({"error" : "Invalid creidentials with the provided token"}, status=status.HTTP_400_BAD_REQUEST)
        except EmailVerificationToken.DoesNotExist:
            return Response({"error" : "invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "facing some tech issues"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"error" : "both fields email and token are required"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_verified(request):
    return Response({"is_verified" : request.user.is_verified()})