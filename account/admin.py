from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(ForgotPasswordToken)
admin.site.register(EmailVerificationToken)
admin.site.register(Profile)