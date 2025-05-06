from django.db import models
from django.utils import timezone
from users.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon_class = models.CharField(max_length=100, default='fa fa-folder' ) # masalan: 'fa fa-code'

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def test_count(self):
        return self.tests.count()

    def __str__(self):
        return self.name


DIFFICULTY_LEVELS = [
    ('easy', "Oson"),
    ('medium', "O'rtacha"),
    ('hard', "Qiyin"),
]


class Test(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='easy')
    is_basics = models.BooleanField(default=True)
    description = models.CharField(max_length=300, default='')
    duration = models.DurationField(default=timezone.timedelta(minutes=20))  # test muddati 20 daqiqa
    # image = models.ImageField(upload_to='test_images/', default='test_images/default.png')
    max_attempt = models.PositiveSmallIntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=(timezone.now()+timezone.timedelta(days=10)))
    pass_percentage = models.PositiveIntegerField(default=60)
    icon_class = models.CharField(max_length=100, default='fa fa-folder' ) # masalan: 'fa fa-code'
    completed_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'test'
        verbose_name_plural = 'tests'

    def question_count(self):
        return self.questions.count()

    def __str__(self):
        return self.title
    

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=500)
    code = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50, default='python')
    a = models.CharField(max_length=300)
    b = models.CharField(max_length=300)
    c = models.CharField(max_length=300)
    d = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=1, help_text='E.x: a')

    class Meta:
        verbose_name = 'question'
        verbose_name_plural = 'questions'

    def __str__(self):
        return f"Question of {self.test}: {self.question}"


class CheckTest(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    correct = models.PositiveSmallIntegerField(default=0)
    incorrect = models.PositiveSmallIntegerField(default=0)
    skipped = models.PositiveSmallIntegerField(default=0)
    is_passed = models.BooleanField(default=False)
    percentage = models.PositiveSmallIntegerField(default=0)
    checked_date = models.DateTimeField(auto_now_add=True)
    spent_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Test of " + self.student.username

    

class CheckQuestion(models.Model):
    checktest = models.ForeignKey(CheckTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    given_answer = models.CharField(max_length=1)
    is_true = models.BooleanField(default=False)
    checked_date = models.DateTimeField(auto_now_add=True)


class Reactions(models.TextChoices):
    NONE = 'None', 'No Reaction'
    LIKE = 'Like', 'Like'
    DISLIKE = 'Dislike', 'Dislike'
    FIRE = 'Fire', 'Fire'


class ReactionTest(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    reaction = models.CharField(
        max_length=10,
        choices=Reactions.choices,
        default=Reactions.NONE
    )

    class Meta:
        verbose_name = 'reaction to test'
        verbose_name_plural = 'reactions to tests'
        unique_together = ('user', 'test')  # foydalanuvchi har testga 1 marta reaksiya

    def __str__(self):
        return f"{self.test.title} - {self.reaction} by {self.user.username}"


class SavedTest(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True )

    class Meta:
        verbose_name = 'saved test'
        verbose_name_plural = 'saved tests'

    def __str__(self):
        return f"{self.test.title} was saved by {self.user.username}. STATUS={self.status}"


class Comment(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return f"{self.test.title} was written by {self.user.username}"


@receiver(pre_save, sender=CheckQuestion)
def check_answer(sender, instance, *args, **kwargs):
    if instance.given_answer == instance.question.correct_answer:
        instance.is_true = True
