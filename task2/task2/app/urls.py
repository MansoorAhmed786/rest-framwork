from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CommentViewSet,
    CreateUserAPIView,
    DocumentViewSet,
    ProjectViewSet,
    TaskViewSet,
)

router = DefaultRouter()
router.register("project", ProjectViewSet, basename="project")
router.register("task", TaskViewSet, basename="task")
router.register("document", DocumentViewSet, basename="document")
router.register("comment", CommentViewSet, basename="comment")
urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", include(router.urls)),
]

admin.site.urls
