# Generated by Django 3.0.3 on 2020-05-05 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0017_warning_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='warning_pic',
            name='state',
            field=models.CharField(default='not pass', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='warning_pic',
            name='pic_name',
            field=models.CharField(max_length=40),
        ),
    ]
