from django.db import models
from myaccounts.models import MyUser


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class GradedAssignment(models.Model):
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.SET_NULL, blank=True, null=True)
    grade = models.FloatField()

    def __str__(self):
        return self.student.username


class Choice(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Question(models.Model):
    question = models.CharField(max_length=200)
    choices = models.ManyToManyField(Choice)
    answer = models.ForeignKey(
        Choice, on_delete=models.CASCADE, related_name='answer', blank=True, null=True)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='questions', blank=True, null=True)
    order = models.SmallIntegerField()

    def __str__(self):
        return self.question

            
    


# Assignment:
#     - title
#     - teacher(FK)

# Gradedassignment:
#     - assignment(FK)
#     - student(FK)
#     - Graded

# Choice:
#     - Choice CharField

# Question:
#     - question char
#     - choice Many?
#     - assignment PK
#     - order 
        