from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class EmailList(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class EmailAddress(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255, blank=True)
    email_list = models.ForeignKey(EmailList, related_name='email_addresses', on_delete=models.CASCADE)

    def __str__(self):
        return self.email

class Campaign(models.Model):
    CATEGORY_CHOICES = [
        ('MARKETING', 'Marketing'),
        ('POLITICAL', 'Political'),
        ('FUNDRAISING', 'Fundraising'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    goal = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    email_list = models.ForeignKey(EmailList, on_delete=models.SET_NULL, null=True, blank=True)
    email_subject = models.CharField(max_length=255, blank=True)
    email_content = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AudienceSegment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    criteria = models.JSONField()  # Store segment criteria as JSON
    campaign = models.ForeignKey(Campaign, related_name='audience_segments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Content(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('SOCIAL', 'Social Media'),
        ('WEB', 'Web'),
    ]

    campaign = models.ForeignKey(Campaign, related_name='contents', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"