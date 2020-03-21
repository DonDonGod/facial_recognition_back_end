from django.db import models

# Create your models here.
# Test
class cal(models.Model):
    valueA = models.CharField(max_length=10)
    valueB = models.CharField(max_length=10)
    result = models.CharField(max_length=10)

class user(models.Model):
    admin = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=20)

# Python manage.py makemigrations
# python manage.py migrate