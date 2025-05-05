from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Quiz, Question, AnswerOption, UserAnswer, Result

# Register User model with default UserAdmin
admin.site.register(User, UserAdmin)

# Custom QuizAdmin
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

# Custom QuestionAdmin
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    list_filter = ('quiz',)

# Custom AnswerOptionAdmin
@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('question', 'is_correct')

# UserAnswer - default admin
@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'question', 'selected_option')
    list_filter = ('user', 'quiz')

# Custom ResultAdmin
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'total')
    list_filter = ('quiz', 'user')


