# apps/users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TeamViewSet, ActivityLogViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'activity-logs', ActivityLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]