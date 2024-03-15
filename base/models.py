from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User Model"""
    name = models.CharField(max_length=200, null=True, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="default.jpg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
