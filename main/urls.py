from django.urls import path
from .views import (
    IndexView,
    TestsView,
    ResultView,
    PageNotFoundView,
    AboutView,
    ReadyToTestView,
    TestView,
    GetStartedTestsView,
    ExploreTestsView,
    NewCategoryView,
    NewTestView,
    NewQuestionView,
    CategoryView,
)

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:test_id>/test', TestView.as_view(), name='test'),
    path('tests', TestsView.as_view(), name='tests'),
    path('<int:checktest_id>/result', ResultView.as_view(), name='result'),
    path('error/404', PageNotFoundView.as_view(), name='error_404'),
    path('about', AboutView.as_view(), name='about'),
    path('<int:test_id>/ready_to_test', ReadyToTestView.as_view(), name='ready_to_test'),
    path('get-started', GetStartedTestsView.as_view(), name='get_started'),
    path('explore', ExploreTestsView.as_view(), name='explore'),
    path('new-category', NewCategoryView.as_view(), name='new_category'),
    path('new-test', NewTestView.as_view(), name='new_test'),
    path('new-question', NewQuestionView.as_view(), name='new_question'),
    path('category/<str:category_name>', CategoryView.as_view(), name='category'),
]