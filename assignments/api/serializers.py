from assignments.models import Assignment, Question, Choice
from rest_framework import serializers
from myaccounts.models import MyUser


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('choice_title',)


class QuestionSerializer(serializers.ModelSerializer):
    # choice = serializers.StringRelatedField(many=True)
    choices_of_question = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'
        # fields = ('question_text', 'order', 'answer',)

class AssignmentSerializer(serializers.ModelSerializer):
    # title = serializers.StringRelatedField(many=False)
    # teacher = serializers.StringRelatedField(many=False)
    # questions = serializers.SerializerMethodField()
    questions_of_assignment = QuestionSerializer(many=True)

    class Meta:
        model = Assignment
        fields = '__all__'

    def create(self, validated_data):

        questions_data = validated_data.pop('questions_of_assignment')
        # choices = validated_data.pop('choices', [])
        assignment = Assignment.objects.create(**validated_data)
        if questions_data is not None:
            for question_data in questions_data:
                choices_data = question_data.pop('choices_of_question')
                created_question = Question.objects.create(assignment=assignment, **question_data)

                if choices_data is not None:
                    for choice_data in choices_data:
                        created_choice = created_question.choices_of_question.create(**choice_data)
            return assignment


        
# class AssignmentSerializer(serializers.ModelSerializer):
#     questions = serializers.SerializerMethodField()
#     # teacher = StringSerializer(many=False)

#     class Meta:
#         model = Assignment
#         fields = ('__all__')

#     def get_questions(self, obj):
#         questions = QuestionSerializer(obj.questions.all(),
#         many=True).data
#         return questions

#     def create(self, request):
#         data = request.data

#         assignment = Assignment()
#         teacher = MyUser.objects.get(email=data['teacher'])
#         assignment.teacher = teacher
#         assignment.title = data['title']
#         assignment.save()

#         order = 1
#         for q in data['questions']:
#             newQ = Question()
#             newQ.question = q['title']
#             newQ.order = order
#             newQ.save()

#             for c in q['choices']:
#                 newC = Choice()
#                 newC.title = c
#                 newC.save()
#                 newQ.choices.add(newC)

#             newQ.answer = Choice.objects.get(title=q['answer'])
#             newQ.assignment = assignment
#             newQ.save()
#             order += 1
#         return assignment