from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import User, City, BlogPost
from .forms import MyUserCreationFrom, CreateBlogForm


def home(request):
    """Home Page"""
    posts = BlogPost.objects.all()
    context = {
        'title': 'Home',
        'posts': posts
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


@login_required(login_url='login')
def createBlog(request):
    """Post Blog Form"""
    form = CreateBlogForm()
    if request.method == "POST":
        form = CreateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
        return redirect('home');

    context = {
        'form': form,
        'title': 'Create Blog'
    }
    return render(request, 'create-blog.html', context)


def blog(request, pk):
    """Blog Post Page"""
    post = get_object_or_404(BlogPost, id=int(pk))
    context = {
        'title': post.title,
        'post': post
    }
    return render(request, 'blog.html', context)


def updateBlog(request, pk):
    """Update Blog Page"""
    post = get_object_or_404(BlogPost, id=int(pk))
    form = CreateBlogForm(instance=post)
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES, instance=post);
        form.save()
        return redirect('blog', pk=pk)
    context = {
        'title': 'Update Blog',
        'form': form,
        'post': post,
    }
    return render(request, 'create-blog.html', context)