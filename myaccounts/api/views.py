from rest_framework import generics, permissions, viewsets

from ..models import MyUser, Profile
from .serializers import MyUserSerializer, ProfileSerializer


class MyUserCreateView(generics.CreateAPIView):

    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    authentication_classes = ()
    permission_classes = ()


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    permission_classes = (permissions.AllowAny, )


class ProfileStudentView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
