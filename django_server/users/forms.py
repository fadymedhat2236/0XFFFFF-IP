from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserRegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email','password1', 'password2', 'studentIdImage' , 'nationalIdImage']



class UserChangingForm(UserChangeForm):

	class Meta:
		model = User
		fields = ['username', 'email', 'studentIdImage' , 'nationalIdImage']
