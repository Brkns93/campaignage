# apps/users/serializers.py

from rest_framework import serializers
from .models import User, UserProfile, Team, ActivityLog

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'preferences']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'organization', 'is_active', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        return user

class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'members', 'created_at', 'updated_at']

class ActivityLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'action', 'timestamp', 'details']
