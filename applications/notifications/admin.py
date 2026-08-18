from django.contrib import admin

from utils.admin import CloneAdminMixin
from .models import Onboarding, Lapsed, UserInfo, Reminder, LocalNotification


@admin.register(Onboarding, site=admin.site)
class OnboardingAdmin(CloneAdminMixin, admin.ModelAdmin):
    clone_name_field = "copy"
    list_display = ("day", "activity_type", "copy")
    list_filter = ("activity_type",)


@admin.register(Lapsed, site=admin.site)
class LapsedAdmin(CloneAdminMixin, admin.ModelAdmin):
    clone_name_field = "ident"
    list_display = ("ident", "activity_type", "days", "copy")
    list_filter = ("activity_type",)


@admin.register(Reminder, site=admin.site)
class ReminderAdmin(CloneAdminMixin, admin.ModelAdmin):
    clone_name_field = "copy"
    list_display = ("activity_type", "copy")
    list_filter = ("activity_type",)


admin.site.register(UserInfo)
admin.site.register(LocalNotification)
