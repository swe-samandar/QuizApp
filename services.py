from django.utils import timezone
from users.models import MedalChoices, CustomUser
from main.models import CheckQuestion, CheckTest
from core import settings
from threading import Thread
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
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
    subject = "🔐 Parolni tiklash kodingiz"
    from_email = settings.EMAIL_HOST_USER
    to = [user_email]
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <div style="text-align: center;">
                <h1 style="margin-bottom: 10px;">🧠 TestLib</h1>
                <h2 style="color: #333;">Parolni tiklash</h2>
            </div>
            <p style="font-size: 16px;">Assalomu alaykum,</p>
            <p style="font-size: 16px;">Sizning <strong>parolni tiklash kodingiz</strong> quyidagicha:</p>
            <div style="text-align: center; margin: 20px 0;">
                <span style="display: inline-block; font-size: 28px; font-weight: bold; color: #2c3e50; padding: 10px 20px; border: 2px dashed #2c3e50; border-radius: 8px;">{code}</span>
            </div>
            <p style="font-size: 16px;">Kod <strong>5 daqiqa</strong> davomida amal qiladi.</p>
            <hr style="margin: 30px 0;" />
            <p style="font-size: 14px; color: #777;">Bu xat <strong>TestLib</strong> platformasi tomonidan yuborildi. Agar siz bu so‘rovni yubormagan bo‘lsangiz, iltimos, ushbu xatni e'tiborsiz qoldiring.</p>
            <p style="font-size: 14px; color: #777;">🌐 <a href="https://testlib.uz" style="color: #007BFF; text-decoration: none;">testlib.uz</a></p>
        </div>
    </body>
    </html>
    """

    # Fallback plain text
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_with_thread(addresses, message):
    if isinstance(addresses, str):
        addresses = [addresses]

    for address in addresses:
        if is_valid_email(address):
            thread = Thread(target=send_code_via_email, args=(address, message), daemon=True)
            thread.start()
        else:
            print(f"{address} noto'g'ri manzil!")