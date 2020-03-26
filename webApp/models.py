from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.
# Test
class USER(models.Model):
    admin = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=100)

# Receive the pre_delete signal and delete the file associated with the model instance.

@receiver(pre_delete, sender=IMG)
def IMG_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.img.delete(False)


# python manage.py makemigrations
# python manage.py migrate

# set global time_zone='+8:00';