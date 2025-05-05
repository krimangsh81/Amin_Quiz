from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Quiz, Question, AnswerOption, UserAnswer, Result
from .serializers import QuizSerializer, UserAnswerSerializer, ResultSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.db import models

User = get_user_model()

class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubmitAnswerView(generics.CreateAPIView):
    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        answers = request.data.get("answers")  # expects a list of {question_id, selected_option_id}
        quiz_id = request.data.get("quiz_id")

        score = 0
        total = 0

        for ans in answers:
            question = Question.objects.get(id=ans["question_id"])
            selected_option = AnswerOption.objects.get(id=ans["selected_option_id"])
            is_correct = selected_option.is_correct
            total += 1
            if is_correct:
                score += 1
            UserAnswer.objects.create(
                user=user,
                quiz_id=quiz_id,
                question=question,
                selected_option=selected_option
            )
        Result.objects.create(user=user, quiz_id=quiz_id, score=score, total=total)
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "admin_dashboard",
            {
                "type": "score_update",
                "data": {
                    "user": user.username,
                    "quiz": Quiz.objects.get(id=quiz_id).title,
                    "score": score,
                    "total": total
                }
            }
        )
        return Response({"message": "Answers submitted", "score": score, "total": total}, status=status.HTTP_201_CREATED)

class ReviewQuizView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, quiz_id):
        user = request.user
        quiz = Quiz.objects.prefetch_related("question_set__answeroption_set").get(id=quiz_id)
        review = []

        for question in quiz.question_set.all():
            user_answer = UserAnswer.objects.filter(user=user, question=question).first()
            correct_option = question.answeroption_set.filter(is_correct=True).first()

            review.append({
                "question": question.text,
                "options": [
                    {
                        "id": opt.id,
                        "text": opt.text,
                        "is_correct": opt.is_correct,
                        "is_selected_by_user": user_answer.selected_option.id == opt.id if user_answer else False
                    }
                    for opt in question.answeroption_set.all()
                ]
            })
        return Response({"quiz": quiz.title, "review": review})


class QuizAnalyticsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, quiz_id):
        results = Result.objects.filter(quiz_id=quiz_id)
        data = {
            "total_attempts": results.count(),
            "average_score": round(results.aggregate(avg=models.Avg("score"))["avg"], 2),
            "score_distribution": list(results.values("score").annotate(count=models.Count("id")))
        }
        return Response(data)
    
