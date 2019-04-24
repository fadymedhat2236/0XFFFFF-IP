# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegisterForm, UserChangeForm
from .models import User

class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    form = UserChangeForm
    model = User
    list_display = ['email', 'username', 'studentIdImage', 'nationalIdImage']

admin.site.register(User, CustomUserAdmin)