from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, is_teacher, is_student, password=None, **other_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            is_teacher = is_teacher,
            is_student = is_student
        )
        user.set_password(password)
        user.save(using=self._db)
        print ('MANAGER', user)
        return user

    def create_superuser(self, email, first_name, last_name, is_teacher, is_student, password=None, **other_fields):

        user = self.create_user(
            email,
            password=password,
            first_name = first_name,
            last_name = last_name,
            is_teacher = is_teacher,
            is_student = is_student,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class ProfileManger(models.Manager):
    def create_profile(self, user, student_id):
        profile = self.model(user=user, student_id=student_id)
        profile.save()
        print ('PRO MNR', profile)

        return profile

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_teacher = models.BooleanField()
    is_student = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'is_teacher', 'is_student']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name='profile'
    )
    student_id = models.CharField(max_length=15, blank=True)
    
    objects = ProfileManger()

    def __str__(self):
        return self.user.email
