from rest_framework.routers import DefaultRouter
from .views import (
    AssignmentViewSet,
    AssignmentListView,
    TeacherAssignmentListView,
    GradedAssignmentListView
)
from . import views
from django.urls import path, include

router = DefaultRouter()
router.register(r'', AssignmentViewSet, basename='assignments')

urlpatterns = [
    path('list/', AssignmentListView.as_view()),
    path('teacher/<int:pk>/', TeacherAssignmentListView.as_view()),
    path('graded/<int:pk>/', GradedAssignmentListView.as_view()),
    path('', include(router.urls))    
]