from django.contrib import admin

# Register your models here.
from accounts.models import UserProfile
from blog.models import BlogPost

admin.site.register(UserProfile)

admin.site.register(BlogPost)
