from django.contrib import admin
from .models import User, Tweet, Comment, Like, Follow

admin.site.register(User)
admin.site.register(Tweet)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
