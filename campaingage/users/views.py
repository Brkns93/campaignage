# apps/users/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from .models import UserProfile, Team, ActivityLog
from .serializers import UserSerializer, UserProfileSerializer, TeamSerializer, ActivityLogSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Add this line
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(id=user.id)

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only staff members can create new users.")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance and not request.user.is_staff:
            raise PermissionDenied("You do not have permission to update this user.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only staff members can delete users.")
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['get', 'put', 'patch'])
    def profile(self, request, pk=None):
        user = self.get_object()
        if request.user != user and not request.user.is_staff:
            raise PermissionDenied("You do not have permission to access this profile.")
        
        if request.method == 'GET':
            serializer = UserProfileSerializer(user.profile)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            serializer = UserProfileSerializer(user.profile, data=request.data, partial=request.method=='PATCH')
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()  # Add this line
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(members=self.request.user)

    def perform_create(self, serializer):
        team = serializer.save()
        team.members.add(self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user not in instance.members.all():
            raise PermissionDenied("You must be a team member to update the team.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user not in instance.members.all():
            raise PermissionDenied("You must be a team member to delete the team.")
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            team.members.add(user)
            return Response({"message": "User added to team successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            team.members.remove(user)
            return Response({"message": "User removed from team successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all()  # Add this line
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(user=user)