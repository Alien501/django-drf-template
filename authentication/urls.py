from django.urls import path
from .views import (
    RegistrationAPIView, LoginAPIView, VerifyTokenAPIView, 
    ResendVerificationTokenAPI, ForgotPasswordAPI, ProfileAPIView, 
    LogoutAPIView, api_root
)

urlpatterns = [
    path('', api_root, name='api-root'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/', VerifyTokenAPIView.as_view(), name='verify'),
    path('resend_token/', ResendVerificationTokenAPI.as_view(), name='resend-token'),
    path('forgot_password/', ForgotPasswordAPI.as_view(), name='forgot-password'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
