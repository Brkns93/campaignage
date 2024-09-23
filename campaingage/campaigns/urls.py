from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet, AudienceSegmentViewSet, ContentViewSet

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)
router.register(r'audience-segments', AudienceSegmentViewSet)
router.register(r'contents', ContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]