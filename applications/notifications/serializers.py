from rest_framework import serializers

from applications.notifications.models import (
    Lapsed,
    LocalNotification,
    Onboarding,
    Reminder,
)
from utils.activity import ActivityType, filter_by_activity, resolve_activity


class UserInfoSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=dict(), **kwargs):  # noqa: B006
        return super(UserInfoSerializer, self).__init__(instance, data, **kwargs)  # noqa: PLE0101, UP008

    def to_representation(self, instance):
        return {instance.label: instance.value}


class LapsedSerializer(serializers.ModelSerializer):
    userinfo = serializers.SerializerMethodField()

    class Meta:
        model = Lapsed
        fields = ["ident", "copy", "userinfo", "days", "activity_type"]  # noqa: RUF012

    def get_userinfo(self, obj):
        serializer = UserInfoSerializer(obj.userinfo.all(), many=True, context=self.context)

        # Flaten the list of dictionaries
        result = {}
        for line in serializer.data:
            result.update(line)

        return result


class OnboardingSerializer(serializers.ModelSerializer):
    userinfo = serializers.SerializerMethodField()

    class Meta:
        model = Onboarding
        fields = ["day", "copy", "userinfo", "activity_type"]  # noqa: RUF012

    def get_userinfo(self, obj):
        serializer = UserInfoSerializer(obj.userinfo.all(), many=True, context=self.context)

        # Flaten the list of dictionaries
        result = {}
        for line in serializer.data:
            result.update(line)

        return result


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ["copy", "activity_type"]  # noqa: RUF012


class LocalNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalNotification
        fields = ["slug", "title", "description", "destination", "isLapsed", "activity_type"]  # noqa: RUF012


class NotificationsSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=dict(), **kwargs):  # noqa: B006
        return super(NotificationsSerializer, self).__init__(instance, data, **kwargs)  # noqa: PLE0101, UP008

    def to_representation(self, instance):
        request = self.context.get("request")
        activity = resolve_activity(request) if request is not None else ActivityType.WALKING

        serialized_onboarding = OnboardingSerializer(
            filter_by_activity(Onboarding.objects.prefetch_related("userinfo"), activity),
            many=True,
            context=self.context,
        )

        serialized_lapsed = LapsedSerializer(
            filter_by_activity(Lapsed.objects.prefetch_related("userinfo"), activity),
            many=True,
            context=self.context,
        )

        serialized_reminder = ReminderSerializer(
            filter_by_activity(Reminder.objects.all(), activity),
            many=True,
            context=self.context,
        )

        serialized_local = LocalNotificationSerializer(
            filter_by_activity(LocalNotification.objects.all(), activity),
            many=True,
            context=self.context,
        )

        reminder = ""
        if len(serialized_reminder.data) > 0:
            reminder = next(
                (
                    r.get("copy")
                    for r in serialized_reminder.data
                    if r.get("activity_type", None) == ActivityType.WALKING
                ),
                "",
            )

        return {
            "onboarding": serialized_onboarding.data,
            "lapsed": serialized_lapsed.data,
            "reminders": serialized_reminder.data,
            "reminder": reminder,
            "local": serialized_local.data,
        }
