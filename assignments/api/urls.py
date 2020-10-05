from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet
from . import views
from django.urls import path

router = DefaultRouter()
router.register(r'', AssignmentViewSet, basename='assignments')
urlpatterns = router.urls

# app_name = 'assigments.api'


# urlpatterns = [
#     path('create/', views.assignments_view, name='assignments_view')
# ]