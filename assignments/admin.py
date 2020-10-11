from django.contrib import admin
from assignments.models import Assignment, Question, Choice, GradedAssignment, Answer
from django import forms
# Register your models here.

class AnswerAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choices'].queryset = self.fields['choices'].queryset.filter(question=self.instance.question)
        self.fields['answer'].queryset = self.fields['answer'].queryset.filter(question=self.instance.question)

class AnswerAdmin(admin.ModelAdmin):    
    form = AnswerAdminForm

class AnswerInline(admin.StackedInline):
    model = Answer
    form = AnswerAdminForm
    can_delete = False
    verbose_name = 'Answer'

class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerInline,)
    
class QuestionInline(admin.StackedInline):
    model = Question
    verbose_name_plural = 'Questions'

class AssignmentAdmin(admin.ModelAdmin):
    inlines = (QuestionInline,)


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Choice)
admin.site.register(GradedAssignment)
