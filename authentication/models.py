from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework import status

from utils.send_mail import send_email, send_html_email

import uuid
import jwt

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    username = None

    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('First Name',max_length=255, blank=False)
    last_name = models.CharField('Last Name',max_length=255, blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def get_name(self):
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'{self.first_name}'
    
    def generate_login_response(self):
        payload = {
            'id': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'exp': timezone.now() + timezone.timedelta(days=30),
            'iat': timezone.now()
        }
        
        token = jwt.encode(payload, settings.JWT_KEY, algorithm='HS256')
        response = Response({
            'id': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_joined': self.date_joined,
            'last_login': self.last_login,
        }, status=status.HTTP_200_OK)

        response.set_cookie(key='token', value=token, samesite='Lax', httponly=True, secure=False, domain=settings.COOKIE_DOMAIN)
        return response
    
    
    def send_verification_mail(self):
        verification_token = get_random_string(length=8)
        startingcontent = f"Greetings! <b>{self.first_name}</b>,\n\n Thank you for showing interest in our application. Please click on the confirmation link given below to finish setting up your account."
        endingcontent = f"If you have any general questions for us please do not hesitate to contact us. \n\nWe look forward to having you on board!\n\nWarm Regards,\nTeam App Name"
        link = f"{settings.VERIFICATION_URL}?token={verification_token}&email={self.email}"
        linkcontent = "Click this link to verify your email"
        subject = "Email Verification"
        to_email = self.email
        
        verification, created = VerificationCode.objects.get_or_create(user=self)
        verification.code = verification_token
        verification.save()
        
        send_html_email(
            subject=subject, 
            to_email=to_email, 
            context={
                "startingcontent": startingcontent, 
                "endingcontent": endingcontent, 
                "link": link, 
                "linkcontent": linkcontent,
                "user_name": self.first_name,
                "app_name": "App Name"
            },
            template_name="email/verification_email.html"
        )

    def send_forgot_password_mail(self, new_password):
        verification_code = get_random_string(length=8)
        
        startingcontent = f"We received a request to reset your password for your account. If you didn't make this request, you can safely ignore this email."
        endingcontent = f"If you have any questions or need assistance, please don't hesitate to contact our support team."
        link = f"{settings.PASSWORD_RESET_URL}?token={verification_code}&email={self.email}"
        linkcontent = "Reset Password"
        
        subject = "Password Reset - App Name"
        to_email = self.email
        
        verification, created = ForgetPassword.objects.get_or_create(user=self)
        verification.code = verification_code
        verification.new_password = new_password
        verification.save()
        
        send_html_email(
            subject=subject, 
            to_email=to_email, 
            context={
                "startingcontent": startingcontent,
                "endingcontent": endingcontent,
                "verification_code": verification_code,
                "link": link,
                "linkcontent": linkcontent,
                "user_name": self.first_name,
                "app_name": "App Name"
            },
            template_name="email/forgot_password_email.html"
        )

class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user}"

    
class ForgetPassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    new_password = models.CharField(max_length=128)
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.user}"
    
    def save(self, *args, **kwargs):
        if not self.new_password.startswith('pbkdf2_sha256$'):
            self.new_password = make_password(self.new_password)
        super().save(*args, **kwargs)