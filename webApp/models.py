from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.
# Test
class USER(models.Model):
    student_number = models.IntegerField(max_length=20, default='16200001')
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class ADMIN(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class EMOTION(models.Model):
    question = models.CharField(max_length=20)
    student_number = models.IntegerField(max_length=20, default='16200001')
    emotion = models.CharField(max_length=20)
    result = models.CharField(max_length=20)

class WARNING(models.Model):
    student_number = models.IntegerField(max_length=20, default='16200001')
    times = models.IntegerField(max_length=20)
    score = models.IntegerField(max_length=20)


# python manage.py makemigrations
# python manage.py migrate

# set global time_zone='+8:00';