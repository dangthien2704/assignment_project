from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, date_of_birth, is_teacher, is_student, password=None, **other_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            date_of_birth=date_of_birth,
            is_teacher = is_teacher,
            is_student = is_student,
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, first_name, last_name, phone, date_of_birth, is_teacher, is_student, password=None, **other_fields):

        user = self.create_user(
            email,
            password=password,
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            date_of_birth=date_of_birth,
            is_teacher = is_teacher,
            is_student = is_student,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, unique = True)
    date_of_birth = models.DateField()
    is_teacher = models.BooleanField()
    is_student = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'date_of_birth', 'is_teacher', 'is_student']

    ordering = ('created',)

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
        # related_name='profile',
        # primary_key=True
        # null=True
    )
    student_id = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.user.email


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         global token
#         token = Token.objects.create(user=instance)

        
#     return token
    

# @receiver(post_save, sender=MyUser)
# def create_or_update_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# @receiver(post_save, sender=MyUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)    #after user created it will create profile 
#     # instance.profile.save()

# @receiver(post_save, sender=MyUser)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_admin_profile(sender, instance, created, *args, **kwargs):
#     """Create a matching profile whenever a user object is created."""
#     if created: 
#         profile, new = Profile.objects.get_or_create(user=instance)
#     instance.profile.save()

# def create_profile(sender,**kwargs ):
#     if kwargs['created']:
#         user_profile=Profile(user=kwargs['instance'])
#         user_profile.save()

# post_save.connect(create_profile, sender=MyUser)


# post_save.connect(create_profile,sender=MyUser)
    
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)