from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import User, BlogPost, Comment, Like
from .forms import MyUserCreationFrom, CreateBlogForm, UpdateUserForm


def home(request):
    """Home Page"""
    posts = BlogPost.objects.all()
    for post in posts:
        post.comments = post.comment_set.all()
    user_likes = None;
    if request.user.is_authenticated:
        # Query all like objects of the request user
        user_likes = Like.objects.filter(user=request.user)

    for post in posts:
        # Checks if the user and the blogPost share the same Like object
        post.user_liked = user_likes.filter(blogPost=post).exists() if user_likes else False

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
            return redirect('login')
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
    user_likes = None;
    if request.user.is_authenticated:
        # Query all like objects of the request user
        user_likes = Like.objects.filter(user=request.user)
    post.user_liked = user_likes.filter(blogPost=post).exists() if user_likes else False

    if request.method == 'POST':
        Comment.objects.create(
            user=request.user,
            blogPost=post,
            body=request.POST.get('body')
        )
        return redirect('blog', pk=post.id)

    post_comments = post.comment_set.all().order_by('-created')

    context = {
        'title': post.title,
        'post': post,
        'post_comments': post_comments
    }
    return render(request, 'blog.html', context)


@login_required(login_url='login')
def updateBlog(request, pk):
    """Update Blog Page"""
    post = get_object_or_404(BlogPost, id=int(pk))
    if request.user != post.author:
        return HttpResponse('Unauthorized')
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


@login_required(login_url='login')
def deleteBlog(request, pk):
    """Delete Blog Route"""
    post = get_object_or_404(BlogPost, id=int(pk))
    if request.user != post.author:
        return HttpResponse('Unauthorized')
    if request.method == 'POST':
        post.delete()
        return redirect('home')

    context = {
        'title': f'Delete {post.title}?',
        'obj': post.title
    }
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def updateComment(request, pk):
    """Update Comment Route"""
    comment = get_object_or_404(Comment, id=int(pk))
    if request.user != comment.user:
        return HttpResponse('Unauthorized')
    if request.method == 'POST':
        comment.body = request.POST.get('body')
        comment.edited = True
        comment.save()
        return redirect('blog', pk=comment.blogPost.id)
    context = {
        'title': f'Update Comment "{comment.body[:5]}.."',
        'comment': comment
    }
    return render(request, 'update-comment.html', context)


@login_required(login_url='login')
def deleteComment(request, pk):
    """Delete Comment Route"""
    comment = get_object_or_404(Comment, id=int(pk))
    if request.user != comment.user:
        return HttpResponse('Unauthorized')
    if request.method == "POST":
        comment.delete()
        return redirect('blog', pk=comment.blogPost.id)

    context = {
        'title': f'Delete Comment "{comment.body[:5]}.."?',
        'obj': comment.body
    }
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def likeBlog(request, blog_id):
    """Like Blog Route"""
    post = get_object_or_404(BlogPost, id=int(blog_id))
    Like.objects.create(user=request.user, blogPost=post)
    post.likes += 1
    post.save()
    return JsonResponse({'likes': post.likes})


@login_required(login_url='login')
def unlikeBlog(request, blog_id):
    """Unlike Blog Route"""
    post = get_object_or_404(BlogPost, id=int(blog_id))
    like = Like.objects.filter(user=request.user, blogPost=post).first()
    like.delete()
    post.likes -= 1
    post.save()
    return JsonResponse({'likes': post.likes})


def profilePage(request, pk):
    """Profile Page"""
    user = User.objects.get(id=int(pk))
    context = {
        'title': 'Profile Page',
        'user': user,
    }
    return render(request, 'profile.html', context)
 

@login_required(login_url='login')
def updateProfile(request, pk):
    """Update Profile Route"""
    user = User.objects.get(id=int(pk))
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('update-profile', pk=pk,)
    
    context = {
        'title': 'Update Profile',
        'form': form
    }
    return render(request, 'update-profile.html', context)
