from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# Serializer for creating/updating clients
class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']

# Serializer for creating projects
class ProjectCreateSerializer(serializers.ModelSerializer):
    users = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = Project
        fields = ['name', 'users']

    def validate_users(self, users):
        user_ids = []
        for user in users:
            user_id = user.get('id')
            if not user_id:
                raise serializers.ValidationError('Each user must have an "id".')
            if not User.objects.filter(id=user_id).exists():
                raise serializers.ValidationError(f'User with id {user_id} does not exist.')
            user_ids.append(user_id)
        return user_ids

    def create(self, validated_data):
        users_data = validated_data.pop('users')
        project = Project.objects.create(**validated_data)
        project.users.set(users_data)
        return project


# Serializer for detailed project information
class ProjectDetailSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    client = serializers.CharField(source='client.client_name', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'client', 'users', 'created_at', 'created_by']

class ProjectGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']

# Serializer for project details
class ProjectListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'created_at', 'created_by']


# Serializer for client details including projects
class ClientDetailSerializer(serializers.ModelSerializer):
    projects = ProjectGetSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Client
        fields = ['id', 'client_name','projects', 'created_by', 'created_at', 'updated_at']

class ClientUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_by', 'created_at', 'updated_at']
