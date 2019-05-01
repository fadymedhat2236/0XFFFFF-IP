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

			list = analyze_image(studentIdImage, nationalIdImage)
			if list[0] != True:
				messages.error(request, list[0])
			else:
				name=list[1]
				studentId=list[2]
				nationalId=list[3]

				student = Student.objects.filter(student_id = studentId)
				success = False
				if student:

					
					result=compare_national_ids(student.first().national_id,nationalId)
					if result:
						success=True

					if not success:
						messages.error(request, f"user wasn't verified correctly.. entered student id is {studentId} and entered national id is {nationalId}")
				
					else:
						user = User(username=username, email=email, password=password,
				 		studentIdImage=studentIdRawImage, nationalIdImage=nationalIdRawImage, student_id=student.first())
						user.save()
						messages.success(request, f'Account created for {student.first().name}')
						return redirect('blog-home')


		# else:
		# 	print("NO")
		# 	print(form.cleaned_data)
		# 	field_errors = [ (field.label, field.errors) for field in form]
		# 	print(field_errors)
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form' : form})

def compare_national_ids(db_id,photo_id):
	print(photo_id)
	print(db_id)
	no_of_matched=0

	j=0
	for i in range(len(photo_id)):
		if photo_id[i]==db_id[j]:
			no_of_matched++
			j+=1
		else:
			while photo_id[i]!=db_id[j] and j<len(db_id):
				j+=1
			if(j==len(db_id)):
				break
			else:
				no_of_matched++
				j+=1

		
	print(no_of_matched)
	if no_of_matched>=8:
		return True
	else:
		return False