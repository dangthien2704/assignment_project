from django.contrib import admin
from assignments.models import Assignment, Question, Choice, GradedAssignment, Answer
# Register your models here.

admin.site.register(Assignment)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Choice)
admin.site.register(GradedAssignment)
