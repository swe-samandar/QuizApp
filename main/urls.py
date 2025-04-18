from django.urls import path
from .views import (
    IndexView,
    TestsView,
    ResultView,
    PageNotFoundView,
    AboutView,
    SettingsView,
)

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tests', TestsView.as_view(), name='tests'),
    path('result', ResultView.as_view(), name='result'),
    path('error/404', PageNotFoundView.as_view(), name='error_404'),
    path('about', AboutView.as_view(), name='about'),
    path('settings', SettingsView.as_view(), name='settings'),
]