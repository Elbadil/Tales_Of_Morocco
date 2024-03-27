from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.contrib import messages
from itertools import chain
from operator import attrgetter
from .models import User, BlogPost, Comment, Like, City
from .forms import MyUserCreationFrom, CreateBlogForm, UpdateUserForm


def index(request):
    """Landing Page"""
    return render(request, 'index.html')


def home(request):
    """Home Page"""
    query = request.GET.get('s_query') if request.GET.get('s_query') else ''
    
    posts_list = BlogPost.objects.filter(
        Q(city__name__icontains=query) |
        Q(title__icontains=query) |
        Q(specific_location__icontains=query)
    )

    likes = Like.objects.all()
    comments = Comment.objects.all()

    # paginate the posts
    posts = paginatePosts(request, posts_list)

    # setup likes and comments logic
    postSetup(request, posts)

    # Sort activities
    activities = sortActivities(posts, likes, comments)

    context = {
        'title': 'Home',
        'posts': posts,
        'activities': activities[:12]
    }
    return render(request, 'home.html', context)


def postSetup(request, posts):
    """sets up all necessary posts logic"""
    for post in posts:
        post.comments = post.comment_set.all()

    user_likes = None;
    if request.user.is_authenticated:
        # Query all like objects of the request user
        user_likes = Like.objects.filter(user=request.user)

    for post in posts:
        # Check if the user and the blogPost share the same Like object
        post.user_liked = user_likes.filter(blogPost=post).exists() if user_likes else False


def sortActivities(posts, likes, comments):
    """Create and return all activities"""
    activities = sorted(
        # chain combines the list of objects directly without creating a new list
        chain(posts, comments, likes),
        # attrgetter to only compare the 'created' attribute of the objects
        # instead of the whole objects, which means it provides more control and
        # clarity in specifying the attribute to be used for sorting
        key=attrgetter('created'),
        reverse=True
    )
    return activities


def paginatePosts(request, posts):
    """Paginates a list posts"""
    paginator = Paginator(posts, 3)
    page = request.GET.get('page', 1)
    custom_page = request.GET.get('page-input')
    if custom_page:
        page = custom_page
    posts = paginator.get_page(page)
    return posts


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
            messages.success(request, "Your account has been created! You can now log in")
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


def profilePage(request, pk):
    """Profile Page"""
    user = User.objects.get(id=int(pk))
    posts = BlogPost.objects.filter(author__id=int(pk))
    user_comments = user.comment_set.all()
    user_likes = user.like_set.all()

    # setup likes and comments logic
    postSetup(request, posts)

    # Sort activities
    activities = sortActivities(posts, user_likes, user_comments)

    context = {
        'title': 'Profile Page',
        'user': user,
        'posts': posts,
        'activities': activities[:10]
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def userActivities(request):
    """User Activity Page"""
    user = request.user
    posts = BlogPost.objects.filter(author=user)
    user_comments = user.comment_set.all()
    user_likes = user.like_set.all()

    # Sort activities
    activities = sortActivities(posts, user_likes, user_comments)

    context = {
        'title': 'Profile Page',
        'user': user,
        'activities': activities[:10]
    }
    return render(request, 'user_activity.html', context)


@login_required(login_url='login')
def updateUser(request):
    """Update Profile Route"""
    user = request.user
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully updated your account!')
            return render(request, 'update-profile.html', {'form': form})
    
    context = {
        'title': 'Update Account',
        'form': form
    }
    return render(request, 'update-profile.html', context)


@login_required(login_url='login')
def createBlog(request):
    """Post Blog Form"""
    form = CreateBlogForm()
    cities = City.objects.all()
    if request.method == "POST":
        city_name = request.POST.get('city')
        try:
            city = City.objects.get(name=city_name)
        except:
            context = {
                'form': CreateBlogForm(request.POST, request.FILES),
                'title': 'Create Blog',
                'cities': cities,
                'incorrect_city': city_name
            }
            return render(request, 'create-blog.html', context)

        form_data = request.POST.copy()
        form_data['city'] = city.id
        form = CreateBlogForm(form_data, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Your blog has been successfully created!')
            return redirect('home')

    context = {
        'form': form,
        'title': 'Create Blog',
        'cities': cities
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
    cities = City.objects.all()
    if request.user != post.author:
        return HttpResponse('Unauthorized')
    form = CreateBlogForm(instance=post)
    if request.method == 'POST':
        city_name = request.POST.get('city')
        try:
            city = City.objects.get(name=city_name)
        except:
            context = {
                'form': CreateBlogForm(request.POST, request.FILES),
                'title': 'Update Blog',
                'cities': cities,
                'post': post,
                'incorrect_city': city_name
            }
            return render(request, 'create-blog.html', context)

        form_data = request.POST.copy()
        form_data['city'] = city.id
        form = CreateBlogForm(form_data, request.FILES, instance=post)
        form.save()
        messages.success(request, 'Your blog has been successfully updated!')
        return redirect('blog', pk=pk)

    context = {
        'title': 'Update Blog',
        'form': form,
        'post': post,
        'cities': cities
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
        messages.success(request, "Your Blog has been successfully deleted!")
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
        messages.success(request, "Your Comment has been successfully Updated!")
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
        messages.success(request, "Your Comment has been successfully deleted!")
        return redirect('blog', pk=comment.blogPost.id)

    context = {
        'title': f'Delete Comment "{comment.body[:5]}.."?',
        'obj': comment.body
    }
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def likeBlog(request, blog_id):
    """Like Blog Route"""
    referring_url = request.META.get('HTTP_REFERER')
    if referring_url and 'login' in referring_url:
        return redirect('home')
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


def communityFav(request):
    """Posts By Community Favorites"""
    posts_list = BlogPost.objects.all().order_by('-likes')
    likes = Like.objects.all()
    comments = Like.objects.all()

    # paginate the posts
    posts = paginatePosts(request, posts_list)

    # setup likes and comments logic
    postSetup(request, posts)

    # Sort activities
    activities = sortActivities(posts, likes, comments)

    context = {
        'title': 'Community Favorites',
        'posts': posts,
        'filter': 'Blogs By Community Favorites',
        'slogan': 'Uncover the gems loved by our community.',
        'activities': activities[:12]
    }
    return render(request, 'home.html', context)


def topSpotPicks(request):
    """Top Spots Visited By the Community"""
    # Getting the blogpost count for each City
    cities_blogpost_count = City.objects.annotate(blogpost_count=Count('blogpost'))
    # Sort these by blogpost count
    sorted_cities = cities_blogpost_count.order_by('-blogpost_count')

    context = {
        'title': 'Top Spot Picks',
        # 'activities': activities[:10]
    }
    return render(request, 'home.html', context)


def postByCuisine(request):
    """Posts by Cuisine"""
    posts_list = BlogPost.objects.all().order_by('-food_rating')
    likes = Like.objects.all()
    comments = Like.objects.all()

    # paginate the posts
    posts = paginatePosts(request, posts_list)

    # setup likes and comments logic
    postSetup(request, posts)

    # Sort activities
    activities = sortActivities(posts, likes, comments)

    context = {
        'title': 'Cuisine Delights',
        'posts': posts,
        'filter': 'Blogs By Cuisine Delights',
        'slogan': 'Discover culinary hotspots across Morocco.',
        'activities': activities[:12]
    }
    return render(request, 'home.html', context)


def postByAcc(request):
    """Posts By Accommodation"""
    posts_list = BlogPost.objects.all().order_by('-accommodation_rating')
    likes = Like.objects.all()
    comments = Like.objects.all()

    # paginate the posts
    posts = paginatePosts(request, posts_list)

    # setup likes and comments logic
    postSetup(request, posts)

    # Sort activities
    activities = sortActivities(posts, likes, comments)

    context = {
        'title': 'Accommodation Escapes',
        'posts': posts,
        'filter': 'Blogs By Accommodation Escapes',
        'slogan': 'Find your perfect retreat in Morocco.',
        'activities': activities[:12]
    }
    return render(request, 'home.html', context)


def ciyBlogs(request, pk):
    """Blogs by City Route"""
    city = get_object_or_404(City, id=int(pk))
    posts_list = BlogPost.objects.filter(city=city)
    likes = []
    comments = []
    for post in posts_list:
        likes.extend(post.like_set.all())
        comments.extend(post.comment_set.all())

    # paginate the posts
    posts = paginatePosts(request, posts_list)

    # setup likes and comments logic
    postSetup(request, posts)

    # Sort activities
    activities = sortActivities(posts, likes, comments)

    context = {
        'title': f'{city.name} Blogs',
        'posts': posts,
        'filter': f'{city.name} Blogs',
        'slogan': f'Discover the essence of {city.name}. Dive into a tapestry of experiences.',
        'activities': activities[:10]
    }
    return render(request, 'home.html', context)

def aboutPage(request):
    """About Page"""
    return render(request, 'about.html')

def contactUsPage(request):
    """About Page"""
    return render(request, 'contact_us.html')
