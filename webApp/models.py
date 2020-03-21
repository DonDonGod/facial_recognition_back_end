from django.db import models

# Create your models here.
# Test
class USER(models.Model):
    admin = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=100)

# python manage.py makemigrations
# python manage.py migrate