from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin','Admin')
    )
    username = models.CharField(max_length=150)
    email= models.EmailField(unique=True)
    phone_number = models.IntegerField()
    role = models.CharField( max_length=10, choices=ROLE_CHOICES, default='user')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    