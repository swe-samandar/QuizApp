from django.urls import path
from .views import (
    DashboardView,
    ProfileView,
    SignUpView,
    LoginView,
    LogoutView,
    SettingsView,
    ChangePasswordView,
    AllResultsView,
    ResetPasswordRequestView,
    VerifyCodeView,
    SetNewPasswordView,
    ToggleSavedTestView
)

app_name = 'users'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('profile/<str:user_username>', ProfileView.as_view(), name='profile'),
    path('signup', SignUpView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('settings', SettingsView.as_view(), name='settings'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
    path('<str:user_username>/all-results', AllResultsView.as_view(), name='all_results'),
    path('reset-password', ResetPasswordRequestView.as_view(), name='reset_password'),
    path('verify-code', VerifyCodeView.as_view(), name='verify_code'),
    path('set-new-password', SetNewPasswordView.as_view(), name='set_new_password'),
    path('toggle-saved-test/', ToggleSavedTestView.as_view(), name='toggle_saved_test')
]