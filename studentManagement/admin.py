from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.
class userModel(UserAdmin):
    pass

admin.site.register(CustomUser,userModel)