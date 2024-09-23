from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailListViewSet, EmailAddressViewSet, CampaignViewSet, AudienceSegmentViewSet, ContentViewSet

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)
router.register(r'audience-segments', AudienceSegmentViewSet)
router.register(r'contents', ContentViewSet)
router.register(r'email-lists', EmailListViewSet)
router.register(r'email-addresses', EmailAddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
]