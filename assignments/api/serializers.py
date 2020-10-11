from assignments.models import *
from rest_framework import serializers
from myaccounts.models import MyUser


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('choice_title',)

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('answer',)

class QuestionSerializer(serializers.ModelSerializer):

    choices_of_question = ChoiceSerializer(many=True)
    answer_of_question = AnswerSerializer(write_only=True) #only show for create or updeat

    class Meta:
        model = Question
        fields = '__all__'


class AssignmentListSerializer(serializers.ModelSerializer): #for list all of assignment without questions
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):

    questions_of_assignment = QuestionSerializer(many=True)
    
    class Meta:
        model = Assignment
        fields = '__all__'

    def create(self, validated_data):
        # choices = question_data.pop('choices') # it's wrong cause question_data haven't define yet
        questions_data = validated_data.pop('questions_of_assignment')
        assignment = Assignment.objects.create(**validated_data)
        order = 0
        for question_data in questions_data:
            choices_data = question_data.pop('choices_of_question')
            answer_data = question_data.pop('answer_of_question')
            created_question = Question.objects.create(assignment=assignment, **question_data)
            created_answer = Answer.objects.create(question = created_question, **answer_data)
            order += 1
            for choice_data in choices_data:
                created_choice = created_question.choices_of_question.create(**choice_data)
        return assignment
   
class GradedAssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradedAssignment
        fields = '__all__'
        # fields = ('grade', 'completed', )


# class CompletedAssignmentSerializer(serializers.ModelSerializer):
#     graded_assignment = GradedAssignmentSerializer()
#     questions_of_assignment = serializers.SerializerMethodField()
#     # answer_of_student = serializers.ChoiceField(
#     #     choices=questions_of_assignment['choices_of_question']
#     #     )
#     class Meta:
#         model = Assignment
#         fields = '__all__'

#     def get_questions_of_assignment(self, obj):
#         questions_of_assignment = QuestionSerializer(obj.questions_of_assignment.all(),
#             many=True).data
#         return questions_of_assignment

#     def create(self, validated_data):
#         correct_answer_count = 0
#         questions = assignment['questions_of_assignment']
#         for question in questions:
#             answer_of_student = serializers.ChoiceField(validated_data.pop('choices_of_question'))
#             if answer_of_student == question['answer_of_question']:
#                 correct_answer_count += 1
        
#         no_of_questions = len(questions)
#         grade = correct_answer_count / no_of_questions * 100
#         completed = True

#         graded_assignment = GradedAssignment.objects.create(**validated_data)
#         return graded_assignment





       