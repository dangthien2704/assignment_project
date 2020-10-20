from assignments.models import *
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

class TakeQuestionSerializer(serializers.ModelSerializer):
    # choices_of_question = ChoiceSerializer(many=True)
    answer_of_question = AnswerSerializer() #only show for create or updeat
    answer_of_student = serializers.CharField(required = False)
    id = serializers.IntegerField()
    class Meta:
        model = Question
        fields = ['id', 'question_title', 'answer_of_question', 'answer_of_student']

class GradedAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradedAssignment
        fields = ('grade', 'completed', )
        extra_kwargs = {
            'grade': {'read_only': True},
            'completed': {'read_only': True}
            }

class TakeAssignmentSerializer(serializers.ModelSerializer):
    
    questions_of_assignment = TakeQuestionSerializer(many=True)
    assignment_id = serializers.IntegerField();
    graded_assignment = GradedAssignmentSerializer()

    class Meta:
        model = Assignment
        fields = ['assignment_id','teacher', 'title',
            'questions_of_assignment', 'graded_assignment']

    def create(self, validated_data): #validated_data == request and use .pop to get list[] 
        # data = request
        # print ('VALIDATED DATA', self.validated_data)
        valid_student = self.context.get('student')

        """This is for getting answer of student list"""
        q_asmt = self.validated_data['questions_of_assignment']
        #or using validated_data.pop('') to get value
        final_answer = []
        for q in q_asmt:
            a_student = q['answer_of_student']
            final_answer.append(a_student)
        # print ('FINAL ANSWER', final_answer)

        """This is for gettings answer of questions from DB"""
        selected_assignment = Assignment.objects.get(pk=self.validated_data['assignment_id'])
        questions_of_assignment = selected_assignment.questions_of_assignment.all()
        answer_of_assignment = []
        for q in questions_of_assignment:
            a = str(q.answer_of_question)
            answer_of_assignment.append(a)
        # print ("ANSWER", answer_of_assignment)

        """Compare answer of student and questions then calculate score"""
        result = 0
        for a,b in zip(final_answer, answer_of_assignment):
            if a == b:
                result += 1
        
        score = result / len(questions_of_assignment) * 10

        self.validated_data['graded_assignment']['grade'] = score  #self is the serializer in views.py
        self.validated_data['graded_assignment']['completed'] = "True"
        
        valid_grade = self.validated_data['graded_assignment']

        # created_grade = GradedAssignment.objects.create(
        #     student=valid_student,
        #     assignment=selected_assignment,
        #     **valid_grade
        # )
        return valid_grade

