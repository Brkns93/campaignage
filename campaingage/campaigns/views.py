from rest_framework import viewsets
from .models import Campaign, AudienceSegment, Content
from .serializers import CampaignSerializer, AudienceSegmentSerializer, ContentSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

class AudienceSegmentViewSet(viewsets.ModelViewSet):
    queryset = AudienceSegment.objects.all()
    serializer_class = AudienceSegmentSerializer

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
