# apps/campaigns/tasks.py

from celery import shared_task
from django.core.mail import send_mass_mail
from django.conf import settings
from django.utils import timezone
from .models import Campaign

@shared_task
def send_campaign_emails(campaign_id):
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        email_list = campaign.email_list
        if not email_list:
            return "No email list attached to the campaign"

        emails = [
            (
                campaign.email_subject,
                campaign.email_content,
                settings.DEFAULT_FROM_EMAIL,
                [email_address.email]
            )
            for email_address in email_list.email_addresses.all()
        ]

        send_mass_mail(emails, fail_silently=False)
        return f"Sent {len(emails)} emails for campaign {campaign.name}"
    except Campaign.DoesNotExist:
        return f"Campaign with id {campaign_id} does not exist"\

@shared_task
def schedule_campaigns():
    now = timezone.now()
    campaigns = Campaign.objects.filter(start_date__lte=now, email_list__isnull=False)
    for campaign in campaigns:
        send_campaign_emails.delay(campaign.id)
    return f"Scheduled {campaigns.count()} campaigns"