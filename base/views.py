from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import MyUserCreationFrom


def home(request):
    """Home Page"""
    context = {
        'title': 'Home'
    }
    return render(request, 'home.html', context)


def loginPage(request):
    """Login Page"""
    # if user is auth redirect home
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Email does not exist')
            return render(request, 'login.html', {'title': 'Login'})
        # check user's credentials using authenticate
        user = authenticate(request, email=email, password=password)
        if not user:
            messages.error(request, 'Login Unsuccessful. Please check your email and password')
        else:
            login(request, user)
            # Check if the user wanted to access page before he were asked to login
            next_page = request.GET.get('next')
            # if so we will be redirecting the user to that page else to home
            return redirect(next_page) if next_page else redirect('home')

    context = {
        'title': 'Login'
    }
    return render(request, 'login.html', context)


def registerPage(request):
    """Register Page"""
    form = MyUserCreationFrom()
    if request.method == 'POST':
        form = MyUserCreationFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form,
        'title': 'Sign Up'
    }
    return render(request, 'register.html', context)


@login_required(login_url='login')
def logoutUser(request):
    """Logout Route"""
    logout(request)
    return redirect(home)
