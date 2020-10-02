from django.urls import path
from .views import (
    ArticleListView,
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleUpdateView
)

urlpatterns = [
    path('', ArticleListView.as_view()),
    path('create', ArticleCreateView.as_view()),   # create url should not have '/' at the end
    path('<pk>', ArticleDetailView.as_view()),
    path('<pk>/update/', ArticleUpdateView.as_view()),
    path('<pk>/delete/', ArticleDeleteView.as_view())
]