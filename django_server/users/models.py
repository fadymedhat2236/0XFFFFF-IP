from django.contrib.auth.models import AbstractUser
from django.db import models




class Student(models.Model):
	student_id = models.CharField(max_length=7, unique=True)
	name = models.CharField(max_length=100)
	national_id = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class User(AbstractUser):
	studentIdImage = models.ImageField(upload_to="images/" )
	nationalIdImage = models.ImageField(upload_to="images/")
	student_id = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.username






