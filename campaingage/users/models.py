# apps/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('CREATOR', 'Creator'),
        ('VIEWER', 'Viewer'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VIEWER')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    organization = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    preferences = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"