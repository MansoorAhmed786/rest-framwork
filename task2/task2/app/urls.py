from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateUserAPIView,ProjectViewSet,TaskViewSet,DocumentViewSet, CommentViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register("project", ProjectViewSet,basename="project")
router.register("task", TaskViewSet,basename="task")
router.register("document", DocumentViewSet,basename="document")
router.register("comment", CommentViewSet,basename="comment")
urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", include(router.urls)),
]

