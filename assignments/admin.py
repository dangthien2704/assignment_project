from django.contrib import admin
from assignments.models import Assignment, Question, Choice, GradedAssignment
# Register your models here.

admin.site.register(Assignment)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(GradedAssignment)
