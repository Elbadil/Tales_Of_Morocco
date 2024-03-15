from django.forms import ModelForm
from .models import User
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
