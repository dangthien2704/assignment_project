from assignments.api.serializers import (
    AssignmentSerializer,
    AssignmentListSerializer,
    GradedAssignmentListSerializer
)
from assignments.models import Assignment, MyUser, GradedAssignment

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status, serializers, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view



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

    def get_queryset(self):
        user = get_object_or_404(MyUser, pk=self.kwargs['pk'])
        return Assignment.objects.filter(teacher=user)

class GradedAssignmentListView(generics.ListAPIView):
    serializer_class = GradedAssignmentListSerializer
    queryset = GradedAssignment.objects.all()
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        user = get_object_or_404(MyUser, pk=self.kwargs['pk'])
        return GradedAssignment.objects.filter(student=user)