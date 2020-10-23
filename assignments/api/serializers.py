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
    graded_assignment = GradedAssignmentSerializer()
    # assignment_id = serializers.IntegerField();

    class Meta:
        model = Assignment
        fields = ['teacher', 'title',
            'questions_of_assignment', 'graded_assignment']

    def create(self, validated_data): #validated_data == request and use .pop to get list[] 
        # data = request
        # print ('VALIDATED DATA', self.validated_data)
        valid_student = self.context.get('student')


        """Getting answer of student list"""
        q_asmt = self.validated_data['questions_of_assignment']
        #or using validated_data.pop('') to get value
        final_answer = []
        for q in q_asmt:
            a_student = q['answer_of_student']['answer_text']
            final_answer.append(a_student)
        # print ('FINAL ANSWER', final_answer)
        
        
        """Getting answer of questions from DB"""
        selected_assignment = Assignment.objects.get(title=self.validated_data['title'])
        questions_of_assignment = selected_assignment.questions_of_assignment.all()
        answer_of_assignment = []
        for q in questions_of_assignment:
            a = str(q.answer_of_question)
            answer_of_assignment.append(a)
        # print ("ANSWER", answer_of_assignment)


        """Comparing answer of student&questions then calculate score"""
        result = 0
        for a,b in zip(final_answer, answer_of_assignment):
            if a == b:
                result += 1
        
        score = result / len(questions_of_assignment) * 10
        print ('SCORE', score)
        self.validated_data['graded_assignment']['grade'] = score  #self is the serializer in views.py
        

        """Calculating progress"""
        completed_question = 0
        for a in final_answer:
            if a != '':
                completed_question += 1
        progress = completed_question/len(questions_of_assignment)*100
        self.validated_data['graded_assignment']['progress'] = "{}%".format(progress)


        """Checking if the assignment has been completed"""    
        if progress < 100:
            self.validated_data['graded_assignment']['completed'] = "False"
        else:
            self.validated_data['graded_assignment']['completed'] = "True"  


        """Creating instance in DB of GradedAssignment"""
        valid_grade = self.validated_data['graded_assignment']
        created_grade = GradedAssignment.objects.create(
            student=valid_student,
            assignment=selected_assignment,
            **valid_grade
        )

        """Creating instance in DB of StudentAnswer"""
        created_studentanswer = StudentAnswer.objects.create(
            student=valid_student,
            assignment=selected_assignment,
            answer_text=final_answer,
            **valid_grade
        )

        return valid_grade


    def update(self, instance, validated_data):
        data = self.validated_data
        student = instance.student
        assignment_id = instance.assignment_id
        graded_instance = student.done_assignment.get(assignment_id=assignment_id)
        print ('GRADED', graded_instance.completed)

        """Getting and UPDATING answer of student"""
        final_answer = []
        for q in data['questions_of_assignment']:
            a_text = q['answer_of_student']['answer_text']
            final_answer.append(a_text)

        instance.answer_text = final_answer


        """Getting answer of questions from DB"""
        selected_assignment = Assignment.objects.get(title=self.validated_data['title'])
        questions_of_assignment = selected_assignment.questions_of_assignment.all()
        answer_of_assignment = []
        for q in questions_of_assignment:
            a = str(q.answer_of_question)
            answer_of_assignment.append(a)


        """Comparing result and UPDATING score"""
        result = 0
        for a,b in zip(final_answer, answer_of_assignment):
            if a == b:
                result += 1
        score = result / len(questions_of_assignment) * 10
        print ('SCORE', score)
        
        instance.grade = score
        graded_instance.grade = score


        """Calculating and UPDATING progress"""
        completed_question = 0
        for a in final_answer:
            if a != '':
                completed_question += 1
        progress = completed_question/len(questions_of_assignment)*100
        
        instance.progress = "{}%".format(progress)
        graded_instance.progress = "{}%".format(progress)


        """Checking and UPDATING completed"""    
        if progress < 100:
            instance.completed = "False"
            graded_instance.completed = "False"
        else:
            instance.completed = "True"  
            graded_instance.completed = "True"

        instance.save()
        graded_instance.save()
        return instance

class PendingAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradedAssignment
        fields = ['assignment', 'grade', 'progress']

    
