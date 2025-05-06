from django.contrib import admin
from .models import Category, Test, Question, CheckTest, CheckQuestion

# Register your models here.

class QuestionInline(admin.TabularInline):
    model = Question


class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['id', 'title', 'author']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'test', 'question', 'correct_answer']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon_class']


class CheckTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'test', 'is_passed', 'correct', 'incorrect', 'percentage']


class CheckQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'checktest', 'question', 'given_answer', 'is_true']


admin.site.register(Test, TestAdmin)
admin.site.register(CheckTest, CheckTestAdmin)
admin.site.register(CheckQuestion, CheckQuestionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)