from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    AssignmentViewSet,
    AssignmentListView,
    TeacherAssignmentListView,
    GradedAssignmentListView,
    TakeAssignmentView,
    PendingAssignmentView,
    TakePendingAssignmentView
)


router = DefaultRouter()
router.register(r'', AssignmentViewSet, basename='assignments')


urlpatterns = [
    path('list/', AssignmentListView.as_view()),
    path('teacher/<int:pk>/', TeacherAssignmentListView.as_view()),
    path('graded/<int:pk>/', GradedAssignmentListView.as_view()),
    path('take/', TakeAssignmentView.as_view()),
    path('pending/<int:pk>/', PendingAssignmentView.as_view()),
    path('take-pending/', TakePendingAssignmentView.as_view()),
    path('', include(router.urls))    
]