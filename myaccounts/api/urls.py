from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('register/', MyUserCreateView.as_view()),
    path('profile/<int:pk>/', ProfileStudentView.as_view()),
    path('users/', include(router.urls))
]
