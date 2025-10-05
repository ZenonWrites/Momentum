from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Project, Objective, DailyCheckIn, Tip, Hobby


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'goal', 'height_cm', 'weight_kg', 
            'body_fat_percentage', 'scheduling_method', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'start_date', 
            'due_date', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ObjectiveSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = Objective
        fields = [
            'id', 'description', 'date', 'is_completed', 
            'completed_at', 'project', 'project_name', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['completed_at', 'created_at', 'updated_at']


class DailyCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyCheckIn
        fields = ['id', 'date', 'mood', 'notes', 'created_at']
        read_only_fields = ['created_at']


class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ['id', 'category', 'source', 'content', 'created_at']
        read_only_fields = ['created_at']


class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name', 'description', 'frequency', 'created_at']
        read_only_fields = ['created_at']


class OnboardingSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    goal = serializers.CharField(max_length=500)
    scheduling_method = serializers.ChoiceField(
        choices=UserProfile.SCHEDULING_CHOICES,
        default='Atomic Habits'
    )

    def create(self, validated_data):
        goal = validated_data.pop('goal')
        scheduling_method = validated_data.pop('scheduling_method', 'Atomic Habits')
        
        user = User.objects.create_user(**validated_data)
        
        UserProfile.objects.create(
            user=user,
            goal=goal,
            scheduling_method=scheduling_method
        )
        
        return user
