from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileUpdateForm, ProfileImageForm, ChangePasswordForm
from main.models import CheckTest, Test
from .models import CustomUser, OTP
from django.contrib.auth import update_session_auth_hash
from services import send_code_via_email, is_valid_email
import random




# Create your views here.

class DashboardView(LoginRequiredMixin, View):
    login_url = 'users:login'
    
    def get(self, request):
        completed_tests = CheckTest.objects.filter(student=request.user).order_by('-checked_date')
        users = CustomUser.objects.all()
    
        users_rank = dict()
        for user in users:
            users_rank[user] = user.point
        users_rank = dict(sorted(users_rank.items(), key=lambda item: item[1], reverse=True))

        user_rank = None
        for index, (user, point) in enumerate(users_rank.items(), start=1):
            if user == request.user:
                user_rank = index
                break
        
        context = {
            'completed_tests': completed_tests,
            'users_rank': users_rank,
            'user_rank': user_rank,
            'recommends':Test.objects.filter(category__in=[test.test.category for test in completed_tests]),
        }
        return render(request, 'users/dashboard.html', context=context)
    

class ProfileView(LoginRequiredMixin, View):
    login_url = 'users:login'
    
    def get(self, request, user_username):
        customuser = get_object_or_404(CustomUser, username=user_username)
        form = ProfileImageForm(instance=customuser)
        completed_tests = CheckTest.objects.filter(student=request.user).order_by('-checked_date')
        users = CustomUser.objects.all()
    
        users_rank = dict()
        for user in users:
            users_rank[user] = user.point
        users_rank = dict(sorted(users_rank.items(), key=lambda item: item[1], reverse=True))

        user_rank = None
        for index, (user, point) in enumerate(users_rank.items(), start=1):
            if user == request.user:
                user_rank = index
                break
        context = {
            'customuser': customuser,
            'completed_tests': completed_tests,
            'users_rank': users_rank,
            'user_rank': user_rank,
            'recommends': Test.objects.filter(category__in=[test.test.category for test in completed_tests]),
            'form': form,
        }
        return render(request, 'users/profile.html', context=context)
    
    def post(self, request, user_username):
        customuser = get_object_or_404(CustomUser, username=user_username)
        form = ProfileImageForm(request.POST, request.FILES, instance=customuser)
        completed_tests = CheckTest.objects.filter(student=request.user).order_by('-checked_date')
        users = CustomUser.objects.all()
    
        users_rank = dict()
        for user in users:
            users_rank[user] = user.point
        users_rank = dict(sorted(users_rank.items(), key=lambda item: item[1], reverse=True))

        user_rank = None
        for index, (user, point) in enumerate(users_rank.items(), start=1):
            if user == request.user:
                user_rank = index
                break
        context = {
            'customuser': customuser,
            'completed_tests': completed_tests,
            'users_rank': users_rank,
            'user_rank': user_rank,
            'recommends': Test.objects.filter(category__in=[test.test.category for test in completed_tests]),
            'form': form,
        }
        if form.is_valid():
            form.save()
            return redirect('users:profile', user_username=user_username)
        
        return render(request, 'users/profile.html', context=context)
    

class SignUpView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'users/register.html', {'form': form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Siz muvaffiqaytli ro'yxatdan o'tdingiz!")
            return redirect('users:login')
        return render(request, 'users/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:index')
            else:
                form.add_error(None, "Noto'g'ri username yoki parol.")
            return redirect('main:index')
        return render(request, 'users/login.html', {'form': form})
    

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main:index')


class SettingsView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request):
        user = request.user
        form = ProfileUpdateForm(instance=user)
        return render(request, 'users/settings.html', {
            'form': form,
        })

    def post(self, request):
        user = request.user
        form = ProfileUpdateForm(request.POST, instance=user)

        if 'cancel' in request.POST:
            messages.info(request, "O'zgarishlar bekor qilindi.")
            return redirect('users:settings')

        if form.is_valid():
            form.save()
            messages.success(request, "Ma'lumotlar muvaffaqiyatli yangilandi!")
            return redirect('users:settings')
        else:
            messages.error(request, "Formada xatoliklar bor. Iltimos, tekshirib qayta yuboring.")
            return render(request, 'users/settings.html', {
                'form': form,
            })


class ChangePasswordView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'users/change_password.html', {'form': form})
    
    def post(self, request):
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return redirect('users:settings')
        return render(request, 'users/change_password.html', {'form': form})


class AllResultsView(LoginRequiredMixin, View):
    login_url = 'users:login'
    def get(self, request, user_username):
        customuser = get_object_or_404(CustomUser, username=user_username)
        completed_tests = CheckTest.objects.filter(student=customuser).order_by('-checked_date')
        context = {
            'completed_tests': completed_tests,
            'customuser': customuser,
        }
        return render(request, 'users/all_results.html', context=context)


class ResetPasswordRequestView(View):
    def get(self, request):
        return render(request, 'users/reset_password.html')

    def post(self, request):
        email = request.POST.get('email')
        if not email or not is_valid_email(email):
            return render(request, 'users/reset_password.html', {'error': "Email noto'g'ri"})

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return render(request, 'users/reset_password.html', {'error': "Bunday foydalanuvchi yo'q"})

        code = f"{random.randint(1000, 9999)}"
        OTP.objects.create(user=user, code=code)
        send_code_via_email(email, code)

        request.session['reset_email'] = email
        return redirect('users:verify_code')  # bu keyingi sahifaga o‘tadi


class VerifyCodeView(View):
    def get(self, request):
        return render(request, 'users/verify_code.html')

    def post(self, request):
        email = request.session.get('reset_email')
        code_input = request.POST.get('code')

        try:
            user = CustomUser.objects.get(email=email)
            otp = OTP.objects.filter(user=user, is_used=False, is_expired=False).last()
            if not otp or otp.code != code_input:
                return render(request, 'users/verify_code.html', {'error': 'Kod noto‘g‘ri'})

            if otp.check_expired():
                return render(request, 'users/verify_code.html', {'error': 'Kod muddati tugagan'})

            otp.is_used = True
            otp.save()
            request.session['reset_verified'] = True
            return redirect('users:set_new_password')
        except:
            return render(request, 'users/verify_code.html', {'error': 'Xatolik yuz berdi'})


class SetNewPasswordView(View):
    def get(self, request):
        if not request.session.get('reset_verified'):
            return redirect('users:reset_password')
        return render(request, 'users/set_new_password.html')

    def post(self, request):
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')
        email = request.session.get('reset_email')
        if password != confirm:
            return render(request, 'users/set_new_password.html', {'error': 'Parollar mos emas'})

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # Foydalanuvchi topilmadi – bu yerda xatolikni qaytaring yoki qayta ishlang
            return render(request, "users/reset_password.html", {"error": "Bunday foydalanuvchi topilmadi"})

        user = CustomUser.objects.get(email=email)
        user.set_password(password)
        user.save()

        # Sessiyalarni tozalash
        request.session.flush()

        return redirect('users:login')  # foydalanuvchini login sahifasiga yuboramiz
