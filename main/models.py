from django.db import models
from django.utils import timezone
from users.models import CustomUser

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Test(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    max_attempt = models.PositiveSmallIntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=(timezone.now()+timezone.timedelta(days=10)))
    pass_percentage = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'test'
        verbose_name_plural = 'tests'

    def __str__(self):
        return self.title
    

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    a = models.CharField(max_length=300)
    b = models.CharField(max_length=300)
    c = models.CharField(max_length=300)
    d = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=300, help_text='E.x: a')

    class Meta:
        verbose_name = 'questoin'
        verbose_name_plural = 'questoins'

    def __str__(self):
        return f"Question of {self.test}: {self.question}"
