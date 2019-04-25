# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegisterForm, UserChangingForm
from .models import User, Student

class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    form = UserChangingForm
    model = User
    list_display = ['email', 'username', 'student_id' , 'studentIdImage', 'nationalIdImage']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ['email', 'username', 'student_id' , 'studentIdImage', 'nationalIdImage'],
        }),
    )

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ['email', 'username', 'student_id' , 'studentIdImage', 'nationalIdImage'],
        }),
    )



admin.site.register(User, CustomUserAdmin)
admin.site.register(Student)
