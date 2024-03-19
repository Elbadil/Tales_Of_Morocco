from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('create-blog/', views.createBlog, name='create-blog'),
    path('update-blog/<str:pk>/', views.updateBlog, name='update-blog'),
    path('delete-blog/<str:pk>/', views.deleteBlog, name="delete-blog"),
    path('blog/<str:pk>/', views.blog, name='blog'),
    path('update-comment/<str:pk>/', views.updateComment, name='update-comment'),
    path('delete-comment/<str:pk>/', views.deleteComment, name='delete-comment'),
    path('like/<str:blog_id>/', views.likeBlog, name='like-blog'),
    path('unlike/<str:blog_id>/', views.unlikeBlog, name='unlike-blog'),
    path('profile/<str:pk>/', views.profilePage, name='profile'),
    path('update-profile/<str:pk>/', views.updateUser, name='update-profile'),
    path('community-fav/', views.communityFav, name='community-fav'),
    path('top-picks/', views.topSpotPicks, name='top-picks'),
    path('cuisine-delights/', views.postByCuisine, name='cuisine-delights'),
    path('accommodation-escapes/', views.postByAcc, name='accommodation-escapes')
]
