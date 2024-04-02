# users/urls.py
from django.urls import path
from .views import UserPhoneNumberCreateView
from home.views import CustomAuthToken 
from .views import UserDetailView,GenerateAccessToken
urlpatterns = [
    path('users/', UserPhoneNumberCreateView.as_view(), name='user-phone-create'),
    path('api/login/', CustomAuthToken.as_view(), name='api_login'),
    path('api/user-detail/',UserDetailView.as_view(), name='user-detail'),
    path('api/token/refresh/', GenerateAccessToken.as_view(), name='token_refresh'),
]





