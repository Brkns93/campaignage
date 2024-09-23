# Generated by Django 3.2.9 on 2024-09-23 23:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='email_content',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='email_subject',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.CreateModel(
            name='EmailList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('email_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_addresses', to='campaigns.emaillist')),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='email_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaigns.emaillist'),
        ),
    ]
