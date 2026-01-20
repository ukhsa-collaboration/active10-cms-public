from rest_framework import serializers

from applications.onboarding.models import *  # noqa: F403


class ReadyToGetStartedSerializer(serializers.ModelSerializer):
    """
    Serializer for ReadyToGetStarted model.
    """

    class Meta:
        model = ReadyToGetStarted  # noqa: F405
        fields = (
            "intro_new_user",
            "intro_migrating_user",
            "motion_fitness",
            "location",
            "notifications",
            "terms_link",
        )


class OnboardingSerializer(serializers.ModelSerializer):
    """
    Serializer for Onboarding CMS model.
    """

    ready_to_get_started = serializers.SerializerMethodField()

    class Meta:
        model = Onboarding  # noqa: F405
        fields = (
            "ready_to_get_started",
            "motion_fitness",
            "location",
            "notifications",
            "goals",
            "about_you",
        )

    def get_ready_to_get_started(self, obj):
        return ReadyToGetStartedSerializer(ReadyToGetStarted.objects.first()).data  # noqa: F405
