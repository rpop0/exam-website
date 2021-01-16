from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from users.models import User
from django.utils import timezone


class Question(SafeDeleteModel, models.Model):
    _safedelete_policy = SOFT_DELETE_CASCADE
    question = models.CharField(max_length=2048)
    question_type = models.IntegerField()
    category = models.IntegerField()
    point_value = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return f'{self.question}'


class Answer(SafeDeleteModel, models.Model):
    _safedelete_policy = SOFT_DELETE_CASCADE
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(max_length=2048)
    correct = models.BooleanField(default=None)
    def __str__(self):
        return f'{self.question} - {self.answer}'

class ExamTemplate(SafeDeleteModel, models.Model):
    _safedelete_policy = SOFT_DELETE_CASCADE
    exam_name = models.CharField(max_length=64)
    questions_one = models.ManyToManyField(Question, related_name="rev_question_one", blank=True)
    questions_two = models.ManyToManyField(Question, related_name="rev_question_two", blank=True)

    def __str__(self):
        return self.exam_name

class Exam(models.Model):
    _safedelete_policy = SOFT_DELETE_CASCADE
    exam_template = models.ForeignKey(ExamTemplate, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_sent = models.DateTimeField(auto_now_add=True, blank=True)
    expired = models.BooleanField(default=False, blank=True)
    marked = models.BooleanField(default=False, blank=True)
    reviewed = models.BooleanField(default=False, blank=True)
    passed = models.BooleanField(default=False, blank=True)
    archived = models.BooleanField(default=False, blank=True)
    turned_in = models.DateTimeField(default=None, blank=True, null=True)
    key = models.CharField(max_length=15)
    points = models.IntegerField(default=0)
    points_open_response = models.IntegerField(default=0)
    handler = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    marked_by = models.CharField(max_length=64, blank=True, default=None, null=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.turned_in}"

class Response(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)
    open_response = models.TextField(max_length=2048, blank=True)
    correct = models.BooleanField(default=True, blank=True)
    review = models.TextField(max_length=2048, blank=True)
    open_response_points = models.IntegerField(default=0, blank=True)
    def __str__(self):
        return f"{self.exam}"
