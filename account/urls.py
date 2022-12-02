from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignUpView.as_view()),
    path('exists/', is_exists, name='is_exists'),
    path('user/<int:pk>/', UserDetails.as_view(), name='is_exists'),

    # forgot password
    path('forgot-password/email/', RequestPaswordResetEmail.as_view(), name='forgot-password-email'),
    path('forgot-password/<token>/', change_password_confirm, name='forgot-password-confirm'),
    path('forgot-password/success/<name>/', change_password_success, name='forgot-password-success'),

    # membership
    path('has-membership/', has_membership, name="has-membership"),
    
]