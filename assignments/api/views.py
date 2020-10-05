from assignments.api.serializers import AssignmentSerializer
from assignments.models import Assignment, Question
from rest_framework import viewsets, permissions, status, generics, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view

# @api_view(['GET', 'POST'])
# def assignments_view(request):

#     if request.method == 'POST':
#         serializer = AssignmentSerializer(data=request.data)
#         if serializer.is_valid():
#             assigment = serializer.save()
#             return Response(assigment, status=status.HTTP_201_CREATED)





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
            assignment = serializer.save()
            if assignment:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



