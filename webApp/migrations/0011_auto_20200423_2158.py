# Generated by Django 3.0.3 on 2020-04-23 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0010_auto_20200421_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='EMOTION',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=20)),
                ('student_number', models.IntegerField(default='16200001', max_length=20)),
                ('emotion', models.CharField(max_length=20)),
                ('result', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='WARNING',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.IntegerField(default='16200001', max_length=20)),
                ('times', models.IntegerField(max_length=20)),
                ('score', models.IntegerField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='SCORE',
        ),
        migrations.AddField(
            model_name='user',
            name='student_number',
            field=models.IntegerField(default='16200001', max_length=20),
        ),
    ]