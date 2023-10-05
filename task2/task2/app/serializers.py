from rest_framework import serializers
from.models import User
from django.utils import timezone
from .models import Profile,Project,Task,Document,Comment,ProjectChoices

class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        role = data.get("role")
        password1 = data.get("password")
        password2 = data.get("password2")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "User with this email already exists. Try again with different email"
            )
        if password1 != password2:
            raise serializers.ValidationError(f"Password and Paasword1 must be same!!!")
        if role not in ProjectChoices.get_roles():
            raise serializers.ValidationError(f"{role} is not valid option")

        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        password2 = validated_data.pop("password2")
        role = validated_data.pop("role")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, role=role)
        return user
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['team_members']

    def validate(self,data):
        start_date = data.get("start_date")
        end_data = data.get("end_date")
        if start_date >= end_data:
            raise serializers.ValidationError("start date can't be before end date!!")
        return data

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

        def validate(self, data):
            status = data.get('status')
            if status not in ProjectChoices.get_status():
                raise serializers.ValidationError(f"{status} is not a valid option")
            return data

  
class DocumentSelializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class CommentSelializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class DocumentRequestSerializer(serializers.Serializer):

    project = serializers.IntegerField()

    def validate(self,data):
        project_id = data.get('project')
        request = self.context.get('request')
        user = request.user
        role = user.profile.role
        if role == 'manager':
            return data
        project = Project.objects.filter(pk=project_id).first()
        if not project:
            raise serializers.ValidationError(f"Project with ID {project_id} does not exist.")
        tasks = Task.objects.filter(project=project).first()
        if not tasks:
            raise serializers.ValidationError(f"Tasks do not exist in the specified project.")
        if tasks.assignee != request.user :
            raise serializers.ValidationError(f"You are not allowed.")
        return data