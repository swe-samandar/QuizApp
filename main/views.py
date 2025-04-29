from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from datetime import datetime
from .models import Test, Question, Category, CheckTest, CheckQuestion
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CategoryForm, TestForm, QuestionForm 
from django.utils import timezone
from services import update_user_info, check_test


def get_today(request):
    today = datetime.date(datetime.today())
    return {'today': today}

# Create your views here.

class IndexView(View):
    def get(self, request):
        popular_tests = Test.objects.all().order_by('-completed_count')
        context = {
            'tests': popular_tests
        }
        return render(request, 'main/index.html', context=context)
    

class TestsView(View):
    def get(self, request):
        tests = Test.objects.all()
        categories = Category.objects.all()

        q = request.GET.get('q')
        category_id = request.GET.get('category')
        difficulty = request.GET.get('difficulty')

        if q:
            tests = tests.filter(title__icontains=q)

        if category_id:
            try:
                tests = tests.filter(category__id=int(category_id))
            except ValueError:
                pass

        if difficulty:
            tests = tests.filter(difficulty=difficulty)

        context = {
            'tests': tests,
            'categories': categories
        }
        return render(request, 'main/tests.html', context=context)


class ResultView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request, checktest_id):
        checktest = get_object_or_404(CheckTest, id=checktest_id)
        questions = CheckQuestion.objects.filter(checktest=checktest)
        incorrects = CheckQuestion.objects.filter(checktest=checktest, is_true=False)
        context = {
            'checktest': checktest,
            'questions': questions,
            'incorrects': incorrects
        }
        return render(request, 'main/result.html', context=context)


class PageNotFoundView(View):
    def get(self, request):
        return render(request, 'main/404.html')
    

class AboutView(View):
    def get(self, request):
        return render(request, 'main/about.html')


class ReadyToTestView(LoginRequiredMixin,View):
    login_url = 'users:login'

    def get(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        return render(request, 'main/ready_to_test.html', {'test':test})
    

class TestView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        questions = Question.objects.filter(test=test)
        attemps = CheckTest.objects.filter(student=request.user, test=test).count()

        if test.max_attempt <= attemps:
            return render(request, 'main/404.html', {'error': "Siz bu testni ishlash uchun hamma imkoniyatdan foydlanib bo'lgansiz!"})

        request.session['start_time'] = timezone.now().isoformat()  # ✅ vaqtni saqlash

        # Start time saqlash
        session_key = f'start_time_{test_id}'
        if session_key not in request.session:
            request.session[session_key] = timezone.now().isoformat()

        start_time = timezone.datetime.fromisoformat(request.session[session_key])
        deadline = start_time + test.duration
        remaining_seconds = int((deadline - timezone.now()).total_seconds())

        if remaining_seconds <= 0:
            return render(request, 'main/404.html', {'error': "Test vaqti tugagan!"})

        context = {
            'test': test,
            'questions': questions,
            'remaining_seconds': remaining_seconds,
        }
        return render(request, 'main/test.html', context=context)

    def post(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        attemps = CheckTest.objects.filter(student=request.user, test=test).count()

        if test.max_attempt <= attemps:
            return render(request, 'main/404.html', {'error': "Siz bu testni ishlash uchun hamma imkoniyatdan foydlanib bo'lgansiz!"})

        # Vaqt tugaganini tekshirish
        session_key = f'start_time_{test_id}'
        if session_key not in request.session:
            return render(request, 'main/404.html', {'error': "Sessiya topilmadi. Testni qayta boshlang."})

        start_time = timezone.datetime.fromisoformat(request.session[session_key])
        if timezone.is_naive(start_time):
            start_time = timezone.make_aware(start_time)

        deadline = start_time + test.duration
        if timezone.now() > deadline:
            return render(request, 'main/404.html', {'error': "Test muddati tugagan. Yangi urinish uchun qayta boshlang."})

        if test.max_attempt > attemps:
            test.completed_count += 1
            test.save()
            questions = Question.objects.filter(test=test)

            # ⚠️ Barcha savollarga javob berilganligini tekshirish
            unanswered = []
            for question in questions:
                answer = request.POST.get(str(question.id))
                if not answer:
                    unanswered.append(question)

            if unanswered:
                context = {
                    'test': test,
                    'questions': questions,
                    'error': "Iltimos, barcha savollarga javob bering!"
                }
                return render(request, 'main/test.html', context=context)

            # ✅ Barcha savollarga javob berilgan bo'lsa:
            spent_seconds = int((timezone.now() - start_time).total_seconds())
            checktest = CheckTest.objects.create(
                student=request.user,
                test=test,
                spent_time=spent_seconds  # 🆕 spent_time ni saqlayapmiz
            )
            for question in questions:
                given_answer = request.POST.get(str(question.id))
                CheckQuestion.objects.create(checktest=checktest, question=question, given_answer=given_answer)

            check_test(checktest)
            update_user_info(request.user, checktest)

            # ✅ Sessiyani tozalab yuboramiz, keyingi urinishga halal bermasligi uchun
            del request.session[session_key]

            return redirect('main:result', checktest_id=checktest.id)

        return render(request, 'main/404.html', {'error': "Siz bu testni ishlash uchun hamma imkoniyatdan foydlanib bo'lgansiz!"})


class GetStartedTestsView(View):
    def get(self, request):
        tests = Test.objects.filter(is_basics=True)
        return render(request, 'main/get_started.html', {'tests': tests})
    

class ExploreTestsView(View):
    def get(self, request):
        tests = Test.objects.filter(is_basics=False)
        return render(request, 'main/explore_tests.html', {'tests': tests})
    

class NewCategoryView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'main/new_category.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:index')
        return render(request, 'main/new_category.html', {'form': form})


class NewTestView(View):
    def get(self, request):
        form = TestForm()
        return render(request, 'main/new_test.html', {'form': form})

    def post(self, request):
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.author = request.user
            test.save()
            return redirect('main:index')
        return render(request, 'main/new_test.html', {'form': form})
    

class NewQuestionView(View):
    def get(self, request):
        form = QuestionForm()
        return render(request, 'main/new_question.html', {'form': form})

    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:index')
        return render(request, 'main/new_question.html', {'form': form})
    

class CategoryView(View):
    def get(self, request, category_name):
        tests = Test.objects.filter(category__name=category_name)
        return render(request, 'main/category.html', {'tests': tests})

