from django.contrib import admin

from applications.onboarding.models import Onboarding, ReadyToGetStarted
from utils.admin import CloneAdminMixin


@admin.register(Onboarding)
class OnboardingAdmin(CloneAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "activity_type")
    list_filter = ("activity_type",)


@admin.register(ReadyToGetStarted)
class ReadyToGetStartedAdmin(CloneAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "activity_type")
    list_filter = ("activity_type",)
