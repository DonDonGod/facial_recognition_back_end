# Generated by Django 3.0.3 on 2020-03-24 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0005_auto_20200321_2248'),
    ]

    operations = [
        migrations.CreateModel(
            name='REC_IMG',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='img')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
