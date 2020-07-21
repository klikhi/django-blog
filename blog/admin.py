from django.contrib import admin

# Register your models here.
from .models import Post, Likes,Comment
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Comment)
