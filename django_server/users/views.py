from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
import matplotlib.pyplot as plt
import cv2
from django_server import settings
import os
import numpy as np

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST, request.FILES)
		if form.is_valid():
			username = form.cleaned_data.get('username')

			
			studentIdImage = cv2.imdecode(np.fromstring(form.cleaned_data.get('studentIdImage').read(), np.uint8), cv2.IMREAD_UNCHANGED)
			nationalIdImage = cv2.imdecode(np.fromstring(form.cleaned_data.get('nationalIdImage').read(), np.uint8), cv2.IMREAD_UNCHANGED)
			plt.imshow(studentIdImage)
			plt.show()
			plt.show(nationalIdImage)
			plt.show()


			form.save()
			messages.success(request, f'Account created for {username}')
			return redirect('blog-home')
		# else:
		# 	print("NO")
		# 	print(form.cleaned_data)
		# 	field_errors = [ (field.label, field.errors) for field in form]
		# 	print(field_errors)
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form' : form})