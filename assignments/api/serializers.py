from assignments.models import Assignment, Question, Choice
from rest_framework import serializers
from myaccounts.models import MyUser

class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.StringRelatedField(many=True)

    class Meta:
        model = Question
        fields = ('id', 'question', 'choices', 'order')

class AssignmentSerializer(serializers.ModelSerializer):
    # title = serializers.StringRelatedField(many=False)
    # teacher = serializers.StringRelatedField(many=False)
    questions = serializers.SerializerMethodField()
    

    class Meta:
        model = Assignment
        fields = ('__all__')

    def get_questions(self, obj):
        questions = QuestionSerializer(obj.questions.all(),
            many=True).data  #obj is assignent, questions is the related_name 
        return questions                                                     #in Question model
        
    def create(self, request):
        data = request.data

        assignment = Assignment()
        
        teacher = MyUser.objects.get(email=data['teacher'])
        assignment.teacher = teacher
        assignment.title = data['title']
        assignment.save()

        order = 1
        for q in data['questions']:
            newQ = Question()
            newQ.question = q['title']
            newQ.order = order
            newQ.save()

            for c in q['choices']:
                newC = Choice()
                newC.title = c['choice']
                newC.save()
                newQ.choices.add(newC)

            newQ.answer = Choice.objects.get(title=q['answer'])
            newQ.assignment = assignment
            newQ.save()
            order += 1
        
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