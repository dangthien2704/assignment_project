from assignments.api.serializers import AssignmentSerializer
from assignments.models import Assignment
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

class AssignmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    permission_classes = (permissions.AllowAny, )

    def create(self, request):
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            assignment = serializer.create(request)
            if assignment:
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)