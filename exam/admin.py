from django.contrib import admin

from safedelete.admin import SafeDeleteAdmin, highlight_deleted
from exam.models import ExamTemplate, Question, Answer, Exam, Response



@admin.register(ExamTemplate)
class ExamTemplateAdmim(admin.ModelAdmin):
    list_display = (highlight_deleted, 'exam_name')


@admin.register(Question)
class QuestionAdmin(SafeDeleteAdmin, admin.ModelAdmin):
    list_display = (highlight_deleted, 'question_type', 'category')

@admin.register(Answer)
class AnswerAdmin(SafeDeleteAdmin, admin.ModelAdmin):
    list_display = (highlight_deleted, 'answer', 'correct')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_sent', 'turned_in', 'key', 'points')

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('exam', 'correct', 'question')
