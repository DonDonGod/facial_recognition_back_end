# Generated by Django 3.0.3 on 2020-04-28 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0012_auto_20200423_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emotion',
            name='student_number',
            field=models.IntegerField(default='16200001'),
        ),
        migrations.AlterField(
            model_name='user',
            name='student_number',
            field=models.IntegerField(default='16200001'),
        ),
        migrations.AlterField(
            model_name='warning',
            name='score',
            field=models.IntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='warning',
            name='student_number',
            field=models.IntegerField(default='16200001'),
        ),
        migrations.AlterField(
            model_name='warning',
            name='times',
            field=models.IntegerField(default='0'),
        ),
    ]
