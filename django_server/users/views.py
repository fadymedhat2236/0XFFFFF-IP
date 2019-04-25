from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
import matplotlib.pyplot as plt
import cv2
from django_server import settings
import os
import numpy as np
from .analyze_image import analyze_image
from .models import Student, User
from django.contrib.auth.hashers import make_password


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST, request.FILES)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = make_password(form.cleaned_data['password1'])
			studentIdRawImage = form.cleaned_data['studentIdImage']
			nationalIdRawImage = form.cleaned_data['nationalIdImage']


			studentIdImage = cv2.imdecode(np.fromstring(form.cleaned_data.get('studentIdImage').read(), np.uint8), cv2.IMREAD_UNCHANGED)
			nationalIdImage = cv2.imdecode(np.fromstring(form.cleaned_data.get('nationalIdImage').read(), np.uint8), cv2.IMREAD_UNCHANGED)

			name, studentId, nationalId = analyze_image(studentIdImage, nationalIdImage)
			student = Student.objects.filter(student_id = studentId)

			success = False

			if student:
				if student.first().national_id==nationalId:
					success = True

			if not success:
				messages.error(request, f"user wasn't verified correctly.. entered student id is {studentId} and entered national id is {nationalId}")
			else:
				user = User(username=username, email=email, password=password, studentIdImage=studentIdRawImage, nationalIdImage=nationalIdRawImage)
				user.save()
				messages.success(request, f'Account created for {name}')
				return redirect('blog-home')

			
		# else:
		# 	print("NO")
		# 	print(form.cleaned_data)
		# 	field_errors = [ (field.label, field.errors) for field in form]
		# 	print(field_errors)
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form' : form})