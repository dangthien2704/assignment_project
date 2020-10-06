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
    # choice = serializers.StringRelatedField(many=True)

    choices_of_question = ChoiceSerializer(many=True)
    answer_of_question = AnswerSerializer()
    # answer_of_question = serializers.StringRelatedField()
    

    class Meta:
        model = Question
        fields = '__all__'


class AssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentSerializer(AssignmentListSerializer):
    # title = serializers.StringRelatedField(many=False)
    # teacher = serializers.StringRelatedField(many=False)
    # questions = serializers.SerializerMethodField()
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
