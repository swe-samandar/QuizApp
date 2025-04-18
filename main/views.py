from django.shortcuts import render
from django.views import View
from datetime import datetime


def get_today(request):
    return datetime.date(datetime.today())

# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'main/index.html')
    

class TestsView(View):
    def get(self, request):
        return render(request, 'main/tests.html')
    

class ResultView(View):
    def get(self, request):
        return render(request, 'main/result.html')
    

class PageNotFoundView(View):
    def get(self, request):
        return render(request, 'main/404.html')
    

class AboutView(View):
    def get(self, request):
        return render(request, 'main/about.html')


class SettingsView(View):
    def get(self, request):
        return render(request, 'main/settings.html')