# Generated by Django 3.0.3 on 2020-04-21 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0009_auto_20200421_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='ADMIN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SCORE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('face_score', models.FloatField(max_length=100)),
                ('emotion_score', models.FloatField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='EMOTION',
        ),
        migrations.DeleteModel(
            name='FACE',
        ),
    ]