
from rest_framework import serializers
from .models import Campaign, AudienceSegment, Content

class AudienceSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudienceSegment
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    audience_segments = AudienceSegmentSerializer(many=True, read_only=True)
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = '__all__'
