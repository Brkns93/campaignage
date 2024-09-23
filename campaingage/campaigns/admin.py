
from django.contrib import admin
from .models import Campaign, AudienceSegment, Content

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'start_date', 'end_date', 'created_by')
    list_filter = ('category', 'start_date', 'end_date')
    search_fields = ('name', 'description')

@admin.register(AudienceSegment)
class AudienceSegmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign')
    list_filter = ('campaign',)
    search_fields = ('name', 'description')

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'campaign')
    list_filter = ('content_type', 'campaign')
    search_fields = ('title', 'body')