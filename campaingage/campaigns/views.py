# apps/campaigns/views.py

from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import EmailList, EmailAddress, Campaign, AudienceSegment, Content
from .serializers import EmailListSerializer, EmailAddressSerializer, CampaignSerializer, AudienceSegmentSerializer, ContentSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

class EmailListViewSet(viewsets.ModelViewSet):
    queryset = EmailList.objects.all()
    serializer_class = EmailListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EmailAddressViewSet(viewsets.ModelViewSet):
    queryset = EmailAddress.objects.all()
    serializer_class = EmailAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(email_list__created_by=self.request.user)

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()  # Add this line
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Update AudienceSegmentViewSet and ContentViewSet similarly
class AudienceSegmentViewSet(viewsets.ModelViewSet):
    queryset = AudienceSegment.objects.all()  # Add this line
    serializer_class = AudienceSegmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(campaign__created_by=self.request.user)

    def perform_create(self, serializer):
        campaign = serializer.validated_data['campaign']
        if campaign.created_by != self.request.user:
            raise PermissionDenied("You do not have permission to create segments for this campaign.")
        serializer.save()

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()  # Add this line
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(campaign__created_by=self.request.user)

    def perform_create(self, serializer):
        campaign = serializer.validated_data['campaign']
        if campaign.created_by != self.request.user:
            raise PermissionDenied("You do not have permission to create content for this campaign.")
        serializer.save()