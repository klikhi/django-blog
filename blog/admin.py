from django.contrib import admin

# Register your models here.
from .models import Post, Likes
admin.site.register(Post)
admin.site.register(Likes)
