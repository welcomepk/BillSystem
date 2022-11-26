from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import User, Customer
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "first_name", "last_name", "email", "shop_name", "phone_no", "address", "date_joined", "gst_no", "adhaar_no", "pan_no", "has_membership" ]


#Serializer to Register User
class RegisterSerializer(ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True)

#   password = serializers.CharField(
#     write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User
    fields = ('email', 'password', 'password2','first_name', 'last_name', 'user_type',
            'shop_name', 'phone_no', 'state', 'dist', 'pan_no', 'gst_no', 'adhaar_no', 'address', 'pincode')
            
    extra_kwargs = {
      'first_name': {'required': True},
      'last_name': {'required': True},
      'shop_name': {'required': True},
      'phone_no': {'required': True},
      'state': {'required': True},
      'dist': {'required': True},
      'pan_no': {'required': True},
      'gst_no': {'required': True},
      'adhaar_no': {'required': True},
      'address': {'required': True},
      'pincode': {'required': True},
      'user_type': {'required': True},
      
    }

  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs

  def create(self, validated_data):
    user = User.objects.create(
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name'],
      gst_no = validated_data['gst_no'],
      pan_no = validated_data['pan_no'],
      state = validated_data['state'],
      dist = validated_data['dist'],
      adhaar_no = validated_data['gst_no'],
      phone_no = validated_data['phone_no'],
      shop_name = validated_data['shop_name'],
      address = validated_data['address'],
      pincode = validated_data['pincode'],
      user_type = validated_data['user_type'],
    )

    user.set_password(validated_data['password'])
    user.save()
    return user



class CustomerSerializer(ModelSerializer):
    class Meta:
      model = Customer
      fields = "__all__"


class RequestPaswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length = 10)

    class Meta:
      fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email = email).exists():
          return super().validate(attrs)
        else:
          raise serializers.ValidationError("Invalid email address")