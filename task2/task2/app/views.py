from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Comment, Document, Project, ProjectChoices, Task
from .serializers import (
    CommentSelializer,
    DocumentRequestSerializer,
    DocumentSelializer,
    ProjectSerializer,
    TaskSerializer,
    UserSignUpSerializer,
)


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        role = user.profile.role
        if role != ProjectChoices.MANAGER:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        user = request.user
        role = user.profile.role
        if role != ProjectChoices.MANAGER:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def list(self, request, *args, **kwargs):
        user = request.user
        rolee = user.profile.role
        if rolee == ProjectChoices.MANAGER:
            queryset = Project.objects.all()
        else:
            queryset = Project.objects.filter(team_members=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        print("delete")
        user = request.user
        rolee = user.profile.role
        if rolee == ProjectChoices.MANAGER:
            instance = self.get_object()
            instance.delete()
        else:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['PUT'])
    def add_assignee(self, request, pk, *args, **kwargs):
        user_id = request.data.get('user_id')
        user = request.user
        role = user.profile.role
        if role != ProjectChoices.MANAGER:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )
        instance = self.get_object()
        project = Project.objects.filter(id=pk)
        project.assignee = user_id
        instance = project
        instance.save()
        return Response(status=status.HTTP_200_OK)


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        role = user.profile.role
        if role != ProjectChoices.MANAGER:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def list(self, request, *args, **kwargs):
        user = request.user
        role = user.profile.role
        if role == ProjectChoices.MANAGER:
            queryset = Task.objects.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        user = request.user
        queryset = Task.objects.filter(assignee=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        rolee = user.profile.role
        if rolee != ProjectChoices.MANAGER:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = request.user
        role = user.profile.role
        if role != ProjectChoices.MANAGER:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def delete(self, request, *args, **kwargs):
        user = request.user
        rolee = user.profile.role
        if rolee != ProjectChoices.MANAGER:
            instance = self.get_object()
            instance.delete()
        else:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['PUT'])
    def add_assignee(self, request, *args, **kwargs):
        user = request.user
        role = user.profile.role
        if role != ProjectChoices.MANAGER:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )

        instance = self.get_object()
        your_field_value = request.data.get('assignee')
        instance.assignee = your_field_value
        instance.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['DELETE'])
    def delete_assignee(self, request, *args, **kwargs):
        user = request.user
        role = user.profile.role
        if role != ProjectChoices.MANAGER:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentViewSet(ModelViewSet):
    serializer_class = DocumentSelializer
    permission_classes = [IsAuthenticated]
    queryset = Document.objects.all()

    def create(self, request, *args, **kwargs):
        request_serializer = DocumentRequestSerializer(
            data=request.data,
            context={'request': request}
        )
        request_serializer.is_valid(raise_exception=True)
        return Response(
            status=status.HTTP_201_CREATED,
            data=request_serializer.data
        )

    def list(self, request, *args, **kwargs):
        user = request.user
        project = Project.objects.filter(team_members=user).first()
        queryset = Document.objects.filter(project=project)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        role = user.profile.role
        if role != ProjectChoices.MANAGER:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = request.user
        role = user.profile.role
        if role != ProjectChoices.MANAGER:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def delete(self, request, *args, **kwargs):
        user = request.user
        rolee = user.profile.role
        if rolee == ProjectChoices.MANAGER:
            instance = self.get_object()
            instance.delete()
        else:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSelializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        role = user.profile.role
        project = Project.objects.filter(team_members=user).first()
        if role != ProjectChoices.MANAGER:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )
        elif project:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data=serializer.data
            )
        elif role == ProjectChoices.MANAGER:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data=serializer.data
            )
        else:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "Project doesnot exist!"}
            )

    def list(self, request, *args, **kwargs):
        user = request.user
        project = Project.objects.filter(team_members=user).first()
        queryset = Comment.objects.filter(project=project)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = request.user
        role = user.profile.role
        if role != ProjectChoices.MANAGER:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=request.data)

    def delete(self, request, *args, **kwargs):
        user = request.user
        rolee = user.profile.role
        if rolee == ProjectChoices.MANAGER:
            instance = self.get_object()
            instance.delete()
        else:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "you dont have permission to access!"}
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
