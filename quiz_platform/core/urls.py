from django.urls import path
from . import views
from .views import QuizListView, SubmitAnswerView, ReviewQuizView, QuizAnalyticsView

urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('submit/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('review/<int:quiz_id>/', ReviewQuizView.as_view(), name='review-quiz'),
    path('analytics/<int:quiz_id>/', QuizAnalyticsView.as_view(), name='quiz-analytics'),
    
]
