# Generated by Django 5.2 on 2025-04-29 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='phone',
        ),
        migrations.AddField(
            model_name='otp',
            name='username',
            field=models.CharField(default='', max_length=128),
        ),
    ]
