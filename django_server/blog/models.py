from django.db import models
from django.utils import timezone
from users.models import User

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title



class Student(models.Model):
	name = models.CharField(max_length=100)
	student_id = models.CharField(max_length=7)
	national_id = models.CharField(max_length=100)

	def __str__(self):
		return self.name




