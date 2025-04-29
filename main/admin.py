from django.contrib import admin
from .models import Category, Test, Question, CheckTest, CheckQuestion

# Register your models here.

class QuestionInline(admin.TabularInline):
    model = Question


class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'author']


class CheckTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'test', 'is_passed', 'correct', 'incorrect', 'percentage']

admin.site.register(Test, TestAdmin)
admin.site.register(CheckTest, CheckTestAdmin)
admin.site.register([Category, Question, CheckQuestion])