# apps/users/views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, UserProfile, Team, ActivityLog
from .serializers import UserSerializer, UserProfileSerializer, TeamSerializer, ActivityLogSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        user = self.get_object()
        serializer = UserProfileSerializer(user.profile)
        return Response(serializer.data)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer

    def get_queryset(self):
        return ActivityLog.objects.filter(user=self.request.user)