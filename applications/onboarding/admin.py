from django.contrib import admin

from applications.onboarding.models import Onboarding, ReadyToGetStarted


@admin.register(Onboarding)
class OnboardingAdmin(admin.ModelAdmin):
    pass


admin.site.register(ReadyToGetStarted)
