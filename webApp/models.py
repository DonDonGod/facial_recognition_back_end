from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.
# Test
class USER(models.Model):
    student_number = models.IntegerField(default='16200001')
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    model_loss = models.FloatField(default='0.01')
    model_acc = models.FloatField(default='0.01')

class ADMIN(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class EMOTION(models.Model):
    question = models.CharField(max_length=20)
    student_number = models.IntegerField(default='16200001')
    emotion = models.CharField(max_length=20)
    result = models.CharField(max_length=20)
    pic_name = models.CharField(max_length=20)
    acc = models.FloatField(default='0.01')

class WARNING(models.Model):
    student_number = models.IntegerField(default='16200001')
    times = models.IntegerField(default='0')
    score = models.FloatField(default='1.0')

class WARNING_PIC(models.Model):
    student_number = models.IntegerField(default='16200001')
    pic_name = models.CharField(max_length=20)
    acc = models.FloatField(default='0.01')

class WARNING_LIST(models.Model):
    student_number = models.IntegerField(default='16200001')
    list = models.CharField(max_length=1000)


# python manage.py makemigrations
# python manage.py migrate

# set global time_zone='+8:00';