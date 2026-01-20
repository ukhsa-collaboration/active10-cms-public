from rest_framework import serializers

from applications.notifications.models import (
    Lapsed,
    LocalNotification,
    Onboarding,
    Reminder,
    UserInfo,
)


class UserInfoSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=dict(), **kwargs):  # noqa: B006
        return super(UserInfoSerializer, self).__init__(instance, data, **kwargs)  # noqa: PLE0101, UP008

    def to_representation(self, instance):
        return {instance.label: instance.value}


class LapsedSerializer(serializers.ModelSerializer):
    userinfo = serializers.SerializerMethodField()

    class Meta:
        model = Lapsed
        fields = ["ident", "copy", "userinfo", "days"]  # noqa: RUF012

    def get_userinfo(self, obj):
        serializer = UserInfoSerializer(
            UserInfo.objects.filter(lapsed=obj.id), many=True, context=self.context
        )

        # Flaten the list of dictionaries
        result = {}
        for line in serializer.data:
            result.update(line)

        return result


class OnboardingSerializer(serializers.ModelSerializer):
    userinfo = serializers.SerializerMethodField()

    class Meta:
        model = Onboarding
        fields = ["day", "copy", "userinfo"]  # noqa: RUF012

    def get_userinfo(self, obj):
        serializer = UserInfoSerializer(
            UserInfo.objects.filter(onboarding=obj.id), many=True, context=self.context
        )

        # Flaten the list of dictionaries
        result = {}
        for line in serializer.data:
            result.update(line)

        return result


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ["copy"]  # noqa: RUF012


class LocalNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalNotification
        fields = ["slug", "title", "description", "destination", "isLapsed"]  # noqa: RUF012


class NotificationsSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=dict(), **kwargs):  # noqa: B006
        return super(NotificationsSerializer, self).__init__(instance, data, **kwargs)  # noqa: PLE0101, UP008

    def to_representation(self, instance):
        serialized_onboarding = OnboardingSerializer(
            Onboarding.objects.all(), many=True, context=self.context
        )

        serialized_lapsed = LapsedSerializer(Lapsed.objects.all(), many=True, context=self.context)

        serialized_reminder = ReminderSerializer(
            Reminder.objects.all(),
            many=True,
            context=self.context,
        )

        serialized_local = LocalNotificationSerializer(
            LocalNotification.objects.all(),
            many=True,
            context=self.context,
        )

        reminder = ""

        if len(serialized_reminder.data) > 0:
            reminder = serialized_reminder.data[0].get("copy")

        return {
            "onboarding": serialized_onboarding.data,
            "lapsed": serialized_lapsed.data,
            "reminder": reminder,
            "local": serialized_local.data,
        }
