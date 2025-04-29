from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class MedalChoices(models.TextChoices):
    NONE = 'None', 'No Medal'
    BRONZE = 'Bronze', 'Bronze Medal'
    SILVER = 'Silver', 'Silver Medal'
    GOLD = 'Gold', 'Gold Medal'

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    phone_number = models.CharField(max_length=17)
    bio = models.CharField(max_length=300, blank=True)
    completed_tests = models.PositiveIntegerField(default=0)
    point = models.PositiveIntegerField(default=100)
    medal = models.CharField(max_length=10, choices=MedalChoices.choices, default=MedalChoices.NONE)
    average_score = models.PositiveIntegerField(default=0)
    streak_count = models.PositiveSmallIntegerField(default=1)
    last_streak_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username


User = get_user_model()

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default='0000')
    is_expired = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def check_expired(self):
        # 5 daqiqa muddat
        expire_time = self.created + timedelta(minutes=5)
        if timezone.now() > expire_time:
            self.is_expired = True
            self.save()
        return self.is_expired
