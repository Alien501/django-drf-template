from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from .authentication import IsAuthenticated


@api_view(['GET'])
def api_root(request, format=None):
    """
    API Root - List all available endpoints
    """
    return Response({
        'authentication': {
            'register': '/api/register/',
            'login': '/api/login/',
            'verify': '/api/verify/',
            'resend_token': '/api/resend_token/',
            'forgot_password': '/api/forgot_password/',
            'profile': '/api/profile/',
            'logout': '/api/logout/',
        },
        'admin': '/admin/',
        'message': 'Welcome to the API! Visit any endpoint to test the browsable interface.',
    })


# Create your views here.
class RegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.send_verification_mail()
        return Response({
            'detail': 'Registration Successful. Please check your email for verification.',
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=status.HTTP_201_CREATED)
    
class VerifyTokenAPIView(APIView):
    def get(self, request):
        email = request.query_params.get('email', '')
        token = request.query_params.get('token', '')
        user = get_object_or_404(User, email=email)
        if user.is_verified:
            return Response({'detail': 'User is already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            v = VerificationCode.objects.get(user=user,code=token)
            user.is_verified=True
            user.save()
            
            return user.generate_login_response()
        except:
            return Response({'detail': 'Invalid Code.'}, status=status.HTTP_400_BAD_REQUEST)
        
class ResendVerificationTokenAPI(APIView):
    def get(self, request):
        email = request.query_params.get('email', '')
        try:
            print(email)
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({'detail': 'User Already Verified'}, status=status.HTTP_400_BAD_REQUEST)
            user.send_verification_mail()
            return Response({'detail': 'Verification code sent to your email'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'detail': 'Both email and password are required',
                'code': 'missing_credentials'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        user = authenticate(request, email=email, password=password)

        
        if user:
            if not user.is_active:
                return Response({
                    'detail': 'Your account is not active.',
                    'code': 'account_inactive'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Check if user is verified
            if not user.is_verified:
                return Response({
                    'detail': 'Please verify your email before logging in. Check your email for verification link.',
                    'code': 'email_not_verified'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            return user.generate_login_response()
            
        else:
            try:
                user = User.objects.get(email=email)
                return Response({
                    'detail': 'Invalid password. Please try again.',
                    'code': 'invalid_password'
                }, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({
                    'detail': 'No account found with this email. If you think it\'s a mistake, please contact the admin.',
                    'code': 'user_not_found'
                }, status=status.HTTP_401_UNAUTHORIZED)
        
class ProfileAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)

        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

        return Response({
            "message": "Success",
            "data": {
                "user": user_data,
            }
        }, status=status.HTTP_200_OK)

class  ForgotPasswordAPI(generics.GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LoginSerializer

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        
        if not email or not password:
            return Response({
                'detail': 'Both email and new password are required',
                'code': 'missing_credentials'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response({
                    'detail': 'Your account is not active. Please verify your email first.',
                    'code': 'account_inactive'
                }, status=status.HTTP_400_BAD_REQUEST)
            user.new_password=password
            user.send_forgot_password_mail(user.new_password)
            return Response({
                'detail': 'Verification code sent to your email',
                'code': 'reset_email_sent'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'detail': 'No account found with this email. Please sign up first.',
                'code': 'user_not_found'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                'detail': 'An error occurred while processing your request. Please try again.',
                'code': 'server_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        email = request.query_params.get('email', '')
        token = request.query_params.get('token', '')
        user = get_object_or_404(User, email=email)

        try:
            f = ForgetPassword.objects.get(user=user,code=token)
            user.password=f.new_password
            user.save()
            
            return user.generate_login_response()
        except:
            return Response({'detail': 'Invalid Code.'}, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutAPIView(APIView):
    authentication_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        response.delete_cookie('token', domain=settings.COOKIE_DOMAIN)
        return response