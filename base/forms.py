from django.forms import ModelForm
from .models import User, BlogPost
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationFrom(UserCreationForm):
    """Custom User Creation Form"""
    class Meta:
        """Class Meta to specify the Model and the fields"""
        model = User
        fields = [
            'name',
            'username',
            'email',
            'password1',
            'password2',
        ]


class CreateBlogForm(ModelForm):
    """Create Travel Blog Form"""
    class Meta:
        """Class Meta to specify the Model and the fields"""
        model = BlogPost
        fields = [
            'title',
            'city',
            'specific_location',
            'description',
            'food',
            'food_rating',
            'accommodation',
            'accommodation_rating',
            'picture'
        ]

class UpdateUserForm(ModelForm):
    """Update Profile From"""
    class Meta:
        """Class Meta to specify the Model and the fields"""
        model = User
        fields = [
            'name',
            'username',
            'email',
            'bio',
            'avatar'
        ]
