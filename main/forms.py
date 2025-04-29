from django import forms
from .models import Question, Test, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['category', 'title', 'difficulty', 'is_basics', 'description', 'max_attempt', 'start_date', 'end_time', 'pass_percentage', 'icon_class']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'is_basics': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'max_attempt': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'pass_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'icon_class': forms.TextInput(attrs={'class': 'form-control'}),
        }


    
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['test', 'question', 'code', 'language', 'a', 'b', 'c', 'd', 'correct_answer']
