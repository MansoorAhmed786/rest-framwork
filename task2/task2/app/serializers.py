from rest_framework import serializers
from.models import User
from django.utils import timezone
from .models import Profile,Project,Task,Document,Comment

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
        if role not in ["manager","QA","developer"]:
            raise serializers.ValidationError(f"{role} is not valid option")

        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        role = validated_data.pop("role")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, role=role)
        return user
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        # fields = '__all__'
        exclude = ['team_members']

    def validate(self,data):
        print("valisate")
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
            if status not in ["open","review","working","awaiting_release","waiting_qa"]:
                raise serializers.ValidationError(f"{status} is not valid option")

            return data
        
class DocumentSelializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class CommentSelializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
