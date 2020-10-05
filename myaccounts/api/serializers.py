from ..models import MyUser, Profile
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['student_id']


class MyUserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()
    password2 = serializers.CharField(
        label='Password confirmation',
        write_only = True,
    )
    
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'department', 'phone', 'password', 'password2', 'profile', 'date_of_birth', 'is_teacher', 'is_student']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')

        if password and password2 and password != password2:
            raise serializers.ValidationError({'password': 'Password does not match!'})
        profile_data = validated_data.pop('profile')
        user = MyUser.objects.create(**validated_data)
        user.set_password(password)   
        user.save()
        """have to put set_password and save otherwise can not login in rest-auth because it won't create password even though user created"""
        profile_data['user'] = user
        profile_instance = Profile.objects.create(**profile_data)
        # profile_instance = Profile.objects.create(user=user,**profile_data)
        return user

        # profile_data = validated_data.pop('profile')
        # user = MyUser.objects.create(**validated_data) # have to put profile instance
        # # Profile.objects.create(user=user, **profile_data)  # means create instance for profile


        # return user



class LoginSerializer(RestAuthLoginSerializer):
    username = None







# class MyUserSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = MyUser
#         fields = ['email', 'first_name', 'last_name', 'department', 'phone', 'password', 'date_of_birth', 'is_teacher', 'is_student']
#         extra_kwargs = {'password': {'write_only': True}}


# class ProfileSerializer(serializers.ModelSerializer):

#     user = MyUserSerializer()
#     class Meta:
#         model = Profile
#         fields = ['user', 'student_id']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         profile = Profile.objects.create(**validated_data) # have to put profile instance
#         MyUser.objects.create(user=user, **user_data)
#         # Profile.objects.create(user = user, **profile_data) # create instance of Profile


#         return profile

