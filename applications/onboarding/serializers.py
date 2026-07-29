from rest_framework import serializers

from applications.onboarding.models import *  # noqa: F403
from utils.activity import ActivityType, pick_by_activity


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
        activity = self.context.get("activity", ActivityType.WALKING)
        rtgs = pick_by_activity(ReadyToGetStarted.objects.all(), activity)
        if rtgs:
            return ReadyToGetStartedSerializer(rtgs).data
        return None


# --- v2 -----------------------------------------------------------------------


class ReadyToGetStartedSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = ReadyToGetStarted  # noqa: F405
        fields = (
            "activity_type",
            "intro_new_user",
            "intro_migrating_user",
            "motion_fitness",
            "location",
            "notifications",
            "terms_link",
        )


class OnboardingSerializerV2(serializers.ModelSerializer):
    """
    Serializer for Onboarding CMS model.

    Served as a list (``many=True``), one entry per activity type the request asks
    for. Unlike v1, ``ready_to_get_started`` is matched to each row's own
    ``activity_type`` rather than to the request's, so a walking and a wheeling
    onboarding in the same response each carry their own get-started copy.
    """

    ready_to_get_started = serializers.SerializerMethodField()

    class Meta:
        model = Onboarding  # noqa: F405
        fields = (
            "activity_type",
            "ready_to_get_started",
            "motion_fitness",
            "location",
            "notifications",
            "goals",
            "about_you",
        )

    def get_ready_to_get_started(self, obj):
        rtgs = pick_by_activity(ReadyToGetStarted.objects.all(), obj.activity_type)
        if rtgs:
            return ReadyToGetStartedSerializerV2(rtgs).data
        return None
