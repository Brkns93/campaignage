# apps/users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, Team, ActivityLog

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

admin.site.register(User, UserAdmin)
admin.site.register(Team)
admin.site.register(ActivityLog)