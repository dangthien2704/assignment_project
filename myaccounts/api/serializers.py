from ..models import MyUser, Profile
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer

from django.contrib.auth import get_user_model

MyUser = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['student_id']


class MyUserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()
    password = serializers.CharField(
        label='Password',
        write_only=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        label='Password confirmation',
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'profile',
                  'password', 'password2', 'is_teacher', 'is_student']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = self.validated_data['password']
        password2 = validated_data.pop('password2')
        student_id = validated_data.pop('profile')
        if password and password2 and password != password2:
            raise serializers.ValidationError(
                {'password': 'Password does not match!'})
        user = MyUser.objects.create_user(**validated_data)
        profile = Profile.objects.create_profile(user=user, **student_id)
        print('PROFILE', profile)
        
        return user


class LoginSerializer(RestAuthLoginSerializer):
    username = None
