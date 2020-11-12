from .serializers import (
    AssignmentSerializer,
    AssignmentListSerializer,
    GradedAssignmentListSerializer,
    TakeAssignmentSerializer,
    # PendingAssignmentSerializer
)

from ..models import Assignment, MyUser, GradedAssignment

from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import views, viewsets, permissions, status, serializers, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError


class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentListSerializer
    queryset = Assignment.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    
class TeacherAssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentListSerializer
    permission_classes = (permissions.IsAuthenticated, )
    ordering = ('assignment',)

    def get_queryset(self, id=None):
        user = get_object_or_404(MyUser, pk=self.kwargs['pk'])
        return Assignment.objects.filter(teacher=user)

class GradedAssignmentListView(generics.ListAPIView):
    serializer_class = GradedAssignmentListSerializer
    queryset = GradedAssignment.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = get_object_or_404(MyUser, pk=self.kwargs['pk'])
        return GradedAssignment.objects.filter(student=user)


"""
The first way. But ListAPIView can not return Response because of loop
so I use the second one
"""
    # class PendingAssignmentView(generics.ListAPIView):

        # def get_queryset(self):
        #     user = get_object_or_404(MyUser, pk=self.request.user.id)
        #     print ('USER', user)
        #     if self.request.user == user:
        #         return GradedAssignment.objects.filter(student=user)


class TakeAssignmentView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request, pk):
        user = get_object_or_404(MyUser, pk=self.kwargs['pk'])
        pending_assignment = GradedAssignment.objects.filter(
            student=user,
            completed=False
            )
        final_serializer = []
        for a in pending_assignment:
            serializer = PendingAssignmentSerializer(a)
            s_data = serializer.data
            final_serializer.append(s_data)

        if request.user == user:
            return Response(final_serializer, status=status.HTTP_200_OK)      
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        data = request.data
        student = request.user 
        student_id = student.id
        assignment_id = data['id']
        print ('DATA', data)
        
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

        # try:
        #     completed_check = student.done_assignment.get(assignment_id=assignment_id)
        #     check_result = completed_check.completed
        #     if check_result == True:
        #         return Response(
        #             {"Information": "This assignment is already complete. You can't take it!"},
        #             status=status.HTTP_412_PRECONDITION_FAILED
        #         )

        # except:
        #     """Validate data then deserialize"""
        #     serializer = TakeAssignmentSerializer(
        #         data=request.data,
        #         context={
        #             'student':student,
        #             'student_id':student_id
        #         }
        #     )

        #     serializer.is_valid()    
        #     taken_assignment = serializer.save()     
        #     if taken_assignment:
        #         return Response(status=status.HTTP_201_CREATED)
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

