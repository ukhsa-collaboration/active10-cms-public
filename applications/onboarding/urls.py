from django.urls import path

from applications.onboarding.views import OnboardingView

urlpatterns = [
    path(r"", OnboardingView.as_view(), name="onboarding"),
]
