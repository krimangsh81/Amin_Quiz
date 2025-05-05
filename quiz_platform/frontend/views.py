from django.shortcuts import render, get_object_or_404, redirect
from core.models import Quiz, Question, AnswerOption, UserAnswer, Result

from django.http import HttpResponseRedirect
from django.urls import reverse


def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})


def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.prefetch_related('answeroption_set')

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        
        user = request.user
        score = 0
        total = questions.count()

        # Process answers submitted in the form
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = AnswerOption.objects.get(id=selected_option_id)
                # Save user answers
                UserAnswer.objects.create(
                    user=user,
                    quiz=quiz,
                    question=question,
                    selected_option=selected_option
                )
                if selected_option.is_correct:
                    score += 1
        
        # Save the quiz result
        Result.objects.create(user=user, quiz=quiz, score=score, total=total)
        
        # Redirect to the result page after the user has submitted their answers
        return HttpResponseRedirect(reverse('quiz_result', kwargs={'pk': quiz.id}))

    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz, 'questions': questions})


def quiz_result(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    result = Result.objects.filter(user=request.user, quiz=quiz).last()
    return render(request, 'quizzes/quiz_result.html', {'quiz': quiz, 'result': result})