from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from api.managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField("email", unique=True)
    provider = models.CharField("provider", max_length=255, blank=False)
    bio = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["provider"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class RefreshToken(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE)
    token = models.CharField(max_length=255)
    expiry_date = models.DateTimeField()
    
    def __str__(self):
        return self.token
