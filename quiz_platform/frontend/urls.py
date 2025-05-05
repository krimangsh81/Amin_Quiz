from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('result/<int:pk>/', views.quiz_result, name='quiz_result'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]
