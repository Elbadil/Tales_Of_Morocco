from django.contrib import admin
from .models import User, City, BlogPost, Comment


admin.site.register(User)
admin.site.register(City)
admin.site.register(BlogPost)
admin.site.register(Comment)
