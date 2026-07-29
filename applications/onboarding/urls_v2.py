from django.urls import path

from applications.onboarding.views import OnboardingV2View

urlpatterns = [
    path("", OnboardingV2View.as_view(), name="onboarding_v2"),
]
