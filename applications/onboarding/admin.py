from django.contrib import admin

from applications.onboarding.models import Onboarding, ReadyToGetStarted
from utils.admin import CloneAdminMixin


@admin.register(Onboarding, site=admin.site)
class OnboardingAdmin(CloneAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "activity_type")
    list_filter = ("activity_type",)


@admin.register(ReadyToGetStarted, site=admin.site)
class ReadyToGetStartedAdmin(CloneAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "activity_type")
    list_filter = ("activity_type",)
