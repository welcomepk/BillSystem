from django.urls import path
from .views import SignUpView, MyTokenObtainPairView, is_exists

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignUpView.as_view()),
    path('exists/', is_exists, name='is_exists'),
]