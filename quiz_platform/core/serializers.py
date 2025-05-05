from rest_framework import serializers
from .models import Quiz, Question, AnswerOption, UserAnswer, Result
from django.contrib.auth import get_user_model

User = get_user_model()

class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(source='answeroption_set', many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'options']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(source='question_set', many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'questions']

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['user', 'quiz', 'question', 'selected_option']

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['user', 'quiz', 'score', 'total']
