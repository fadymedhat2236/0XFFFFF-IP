from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	studentIdImage = models.ImageField(upload_to="images/" )
	nationalIdImage = models.ImageField(upload_to="images/")

	def __str__(self):
		return self.username