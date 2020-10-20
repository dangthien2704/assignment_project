from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import MyUser, Profile
from .serializers import MyUserSerializer, ProfileSerializer
from django.shortcuts import get_object_or_404


class MyUserCreateView(generics.CreateAPIView):

    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)  #get_or_create return tuple value (token, boolen)
        data = serializer.data
        data["token"] = token.key
        headers = self.get_success_headers(serializer.data)
        return Response(data, status = status.HTTP_201_CREATED, headers=headers)
        

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


