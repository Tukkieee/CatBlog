from django.contrib import admin
from .models import Blog, Comment, Category, Likes
# Register your models here.


admin.site.register([Blog, Comment, Category, Likes])

