
from rest_framework import serializers
from .models import EmailList, EmailAddress, Campaign, AudienceSegment, Content

class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ['id', 'email', 'name']

class EmailListSerializer(serializers.ModelSerializer):
    email_addresses = EmailAddressSerializer(many=True, read_only=True)

    class Meta:
        model = EmailList
        fields = ['id', 'name', 'description', 'created_by', 'created_at', 'updated_at', 'email_addresses']

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
    email_list = EmailListSerializer(read_only=True)
    email_list_id = serializers.PrimaryKeyRelatedField(
        queryset=EmailList.objects.all(), source='email_list', write_only=True, required=False
    )

    class Meta:
        model = Campaign
        fields = '__all__'
