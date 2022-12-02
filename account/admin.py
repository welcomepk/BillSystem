from django.contrib import admin
from .models import User, Customer, ForgotPasswordToken, Profile

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(ForgotPasswordToken)
admin.site.register(Profile)