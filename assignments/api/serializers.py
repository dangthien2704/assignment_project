from ..models import *
from rest_framework import serializers
from myaccounts.models import MyUser


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice_title']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['answer']

class QuestionSerializer(serializers.ModelSerializer):

    choices_of_question = ChoiceSerializer(many=True)
    answer_of_question = AnswerSerializer() #only show for create or updeat

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
        fields = ['questions_of_assignment']

    def create(self, validated_data):
        """Creating assignment in DB"""
        # choices = question_data.pop('choices') # it's wrong cause question_data haven't define yet
        questions_data = validated_data.pop('questions_of_assignment')
        assignment = Assignment.objects.create(**validated_data)

        """Creating questions and choices in DB"""
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

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ['answer_text']

class TakeQuestionSerializer(serializers.ModelSerializer):
    # answer_of_question = AnswerSerializer() #only show for create or updeat
    answer_of_student = StudentAnswerSerializer()
    id = serializers.IntegerField()
    class Meta:
        model = Question
        fields = ['id', 'question_title', 'answer_of_student']

class GradedAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradedAssignment
        fields = ['id', 'grade', 'progress', 'completed']
        # extra_kwargs = {
        #     'grade': {'read_only': True},
        #     'completed': {'read_only': True},
        #     'progress': {'read_only': True}
        #     }


class TakeAssignmentSerializer(serializers.ModelSerializer):
    
    questions_of_assignment = TakeQuestionSerializer(many=True)
    # graded_assignment = GradedAssignmentSerializer()
    # assignment_id = serializers.IntegerField();

    class Meta:
        model = Assignment
        fields = ['teacher', 'title', 'questions_of_assignment']

    def create(self, validated_data): #validated_data == request and use .pop to get list[] 
        # data = request
        # print ('VALIDATED DATA', validated_data)
        valid_student = self.context.get('student')
        taken_assignment = Assignment.objects.get(title=validated_data['title'])
        
        """Counting grade"""
        counting = GradedAssignment.graded_objects.compute_grade(
            student=valid_student,
            assignment=taken_assignment,
            validated_data = validated_data
        )


        """Creating or Updating GradedAssignment and StudentAnswer"""
        taken_assignment = GradedAssignment.graded_objects.create(
            student=valid_student,
            assignment=taken_assignment,
            validated_data = validated_data
        )

        return taken_assignment



class PendingAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradedAssignment
        fields = ['assignment', 'grade', 'progress']

    
