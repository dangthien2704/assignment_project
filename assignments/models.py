from django.db import models
from myaccounts.models import MyUser


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Question(models.Model):
    question_title = models.CharField(max_length=200)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE,
        related_name='questions_of_assignment', blank=True, null=True)
    order = models.SmallIntegerField()
    
    def __str__(self):
        return self.question_title

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices_of_question')
    choice_title = models.CharField(max_length=50)

    def __str__(self):
        return self.choice_title

class Answer(models.Model):
    question = models.OneToOneField(
        Question, on_delete=models.CASCADE,
        related_name='answer_of_question', blank=True, null=True)
    choices = models.ManyToManyField(Choice)
    answer = models.ForeignKey(
        Choice, on_delete=models.CASCADE,
        related_name='answer_of_question', blank=True, null=True)  

    
    def __str__(self):
        return self.answer.choice_title

class GradedAssignment(models.Model):
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.SET_NULL,
        related_name='graded_assignment', blank=True, null=True)
    grade = models.FloatField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.student.email
        
        