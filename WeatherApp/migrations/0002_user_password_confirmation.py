# Generated by Django 4.2.3 on 2023-07-08 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeatherApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_confirmation',
            field=models.CharField(default='', max_length=128),
        ),
    ]
