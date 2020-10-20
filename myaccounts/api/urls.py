from .views import MyUserCreateView, ProfileStudentView
from django.urls import path, include
# from myaccounts.api.views import MyUserListView, MyUserView
from rest_framework.routers import DefaultRouter    
from myaccounts.api.views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
# urlpatterns = router.urls

urlpatterns = [
    path('register/', MyUserCreateView.as_view()),
    path('profile/<int:pk>/', ProfileStudentView.as_view()),
    path('users/', include(router.urls))
]