from django.db import models
from myaccounts.models import MyUser


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    question_title = models.CharField(max_length=200)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE,
        related_name='questions_of_assignment', blank=True, null=True)
    
    
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


class CommonInfo(models.Model):
    progress = models.CharField(max_length=4, default="0%")
    completed = models.BooleanField(default=False)
    grade = models.IntegerField(default=0)
    
    class Meta:
        abstract = True

class StudentAnswer(CommonInfo):
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='review_answer')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    answer_text = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return "{} - {}".format(self.student.email, self.assignment)

class GradedAssignment(CommonInfo):
    student = models.ForeignKey(MyUser,
        on_delete=models.CASCADE, related_name='done_assignment')
    assignment = models.ForeignKey(
        Assignment, on_delete=models.SET_NULL,
        related_name='graded_assignment', blank=True, null=True)
    
    def __str__(self):
        return "{} - {}".format(self.student.email, self.assignment)
        
        