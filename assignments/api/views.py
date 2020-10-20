from assignments.api.serializers import (
    AssignmentSerializer,
    AssignmentListSerializer,
    GradedAssignmentListSerializer,
    TakeAssignmentSerializer
)
from assignments.models import Assignment, MyUser, GradedAssignment

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status, serializers, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    permission_classes = (permissions.AllowAny, )

class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentListSerializer
    queryset = Assignment.objects.all()
    permission_classes = (permissions.AllowAny, )
    
class TeacherAssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentListSerializer
    permission_classes = (permissions.AllowAny, )
    ordering = ('assignment',)

    def get_queryset(self, id=None):
        user = get_object_or_404(MyUser, pk=self.kwargs['pk'])
        return Assignment.objects.filter(teacher=user)

class GradedAssignmentListView(generics.ListAPIView):
    serializer_class = GradedAssignmentListSerializer
    queryset = GradedAssignment.objects.all()
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        user = get_object_or_404(MyUser, pk=self.kwargs['pk'])
        return GradedAssignment.objects.filter(student=user)

class TakeAssignmentViewSet(generics.CreateAPIView):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = TakeAssignmentSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request):
        data = request.data
        student = request.user 
        student_id = student.id
        
        try:
            completed_check = student.done_assignment.get(student=student)
            check_result = completed_check.completed
            if check_result == True:
                return Response(
                    {"Information": "This assignment is already complete. You can't take it!"},
                    status=status.HTTP_412_PRECONDITION_FAILED
			    )
            else:
                return Response(
                    {"Information": "You haven't completed the assignment. Please continue!"},
                    status=status.HTTP_412_PRECONDITION_FAILED
			    )

        except:
            """Validate data then deserialize"""
            serializer = TakeAssignmentSerializer(
                data=request.data,
                context={
                    'student':student,
                    'student_id':student_id
                }
            )

            serializer.is_valid()    
            taken_assignment = serializer.save()     
            if taken_assignment:
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)





"""For thick views and thin serializer"""

            # """This is for getting answer of student list"""
            # q_asmt = data['questions_of_assignment']
            # final_answer = []
            # for q in q_asmt:
            #     a_student = q['answer_of_student']
            #     final_answer.append(a_student)
            # # print ('FINAL ANSWER', final_answer)

            # """This is for gettings answer of questions from DB"""
            # selected_assignment = Assignment.objects.get(pk=data['assignment_id'])
            # questions_of_assignment = selected_assignment.questions_of_assignment.all()
            # answer_of_assignment = []
            # for q in questions_of_assignment:
            #     a = str(q.answer_of_question)
            #     answer_of_assignment.append(a)
            # # print ("ANSWER", answer_of_assignment)

            # """Compare answer of student and questions then calculate score"""
            # result = 0
            # for i,j in zip(final_answer, answer_of_assignment):
            #     if i == j:
            #         result += 1
            
            # score = result / len(questions_of_assignment) * 10

            # serializer.validated_data['graded_assignment']['grade'] = score
            # serializer.validated_data['graded_assignment']['completed'] = "True"