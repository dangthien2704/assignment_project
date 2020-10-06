from assignments.api.serializers import AssignmentSerializer, AssignmentListSerializer
from assignments.models import Assignment, MyUser

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

    # def create(self, request):
    #     serializer = AssignmentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         assignment = serializer.save()
    #         if assignment:
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentListSerializer
    queryset = Assignment.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

class TeacherAssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentListSerializer
    permission_classes = (permissions.AllowAny, )
    ordering = ('assignment',)

    def get_queryset(self):
        user = get_object_or_404(MyUser, pk=self.kwargs['pk'])
        return Assignment.objects.filter(teacher=user)
