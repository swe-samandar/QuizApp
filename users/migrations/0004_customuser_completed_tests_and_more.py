# Generated by Django 5.2 on 2025-04-28 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='completed_tests',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_streak_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='medal',
            field=models.CharField(choices=[('None', 'No Medal'), ('Bronze', 'Bronze Medal'), ('Silver', 'Silver Medal'), ('Gold', 'Gold Medal')], default='None', max_length=10),
        ),
        migrations.AddField(
            model_name='customuser',
            name='point',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='rank',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='streak_count',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
