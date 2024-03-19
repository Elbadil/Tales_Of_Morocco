from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class User(AbstractUser):
    """Custom User Model"""
    name = models.CharField(max_length=200, null=True, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="default.jpg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class City(models.Model):
    """City Model"""
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class BlogPost(models.Model):
    """Blog Post Model"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    specific_location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=False, blank=False)
    food = models.CharField(max_length=200, blank=True)
    food_rating = models.IntegerField(null=True, blank=True,
                                      validators=[MinValueValidator(1),
                                                  MaxValueValidator(5)])
    accommodation = models.CharField(max_length=200, blank=True)
    accommodation_rating = models.IntegerField(null=True, blank=True,
                                               validators=[MinValueValidator(1),
                                                           MaxValueValidator(5)])
    picture = models.ImageField(null=True, blank=True)
    likes = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """Comment Model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blogPost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body[:50]


class Like(models.Model):
    """Like Model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blogPost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
