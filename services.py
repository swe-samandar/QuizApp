from django.utils import timezone
from users.models import MedalChoices, CustomUser
from main.models import CheckQuestion, CheckTest
from django.core.mail import send_mail
from core import settings
from threading import Thread
import re

def calculate_point(checktest):
    points = 0
    if checktest.is_passed:
        if checktest.test.difficulty == 'easy':
            points += 50
            ball = 2
        elif checktest.test.difficulty == 'medium':
            points += 60
            ball = 4
        elif checktest.test.difficulty == 'hard':
            points += 70
            ball = 6
        points += checktest.correct * ball

    return points


def check_test(checktest):
    questions = CheckQuestion.objects.filter(checktest=checktest)

    total = questions.count()
    correct = questions.filter(is_true=True).count()
    incorrect = total - correct

    checktest.correct = correct
    checktest.incorrect = incorrect

    if total > 0:
        checktest.percentage = correct * 100 // total
        checktest.is_passed = checktest.test.pass_percentage <= checktest.percentage

    checktest.save(update_fields=['correct', 'incorrect', 'percentage', 'is_passed'])


def update_user_info(user, checktest):
    user = CustomUser.objects.filter(username=user.username).first()
    today = timezone.now().date()
    completed_tests = CheckTest.objects.filter(student=user).order_by('-checked_date')

    # user.average_score ni yangilaydi.
    try:
        average_score = sum(test.percentage for test in completed_tests) // completed_tests.count()
    except:
        average_score = 0
    user.average_score = average_score

    # user.point ni yangilaydi.
    user.point += calculate_point(checktest)

    # user ning `streak_count` va `last_streak_date` ini yangilaydi.
    if user.last_streak_date:
        if today == user.last_streak_date + timezone.timedelta(days=1):
            user.streak_count += 1
        elif today == user.last_streak_date:
            pass
        else:
            user.streak_count = 1
    else:
        user.streak_count = 1
    user.last_streak_date = today

    # user.completed_tests ni yangilaydi.
    user.completed_tests += 1 

    # user.medalni yangilaydi.
    if user.point >= 500:
        user.medal = MedalChoices.GOLD
    elif user.point >= 250:
        user.medal = MedalChoices.SILVER
    else:
        user.medal = MedalChoices.BRONZE
    user.save()


# Email uchun regex
REGEX_EMAIL = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

# Emailni tekshiruvchi funksiya
def is_valid_email(email: str) -> bool:
    return re.match(REGEX_EMAIL, email) is not None

def send_code_via_email(user_email, code):
    subject = "Password Reset Code"
    message = f"Assalomu alaykum,\n\nSizning parolni tiklash kodingiz: {code}\n\nKod 5 daqiqa davomida amal qiladi."
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [user_email], fail_silently=False)

def send_with_thread(addresses, message):
    if isinstance(addresses, str):
        addresses = [addresses]

    for address in addresses:
        if is_valid_email(address):
            thread = Thread(target=send_code_via_email, args=(address, message), daemon=True)
            thread.start()
        else:
            print(f"{address} noto'g'ri manzil!")