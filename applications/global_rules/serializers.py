from rest_framework import serializers

from applications.global_rules.models import (
    Accessibility,
    AppVersion,
    Link,
    MissingData,
    TermsConditions,
)


class AppVersionSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=dict(), **kwargs):  # noqa: B006
        return super(AppVersionSerializer, self).__init__(instance, data, **kwargs)  # noqa: PLE0101, UP008

    def to_representation(self, instance):
        return {
            instance.app.name: {
                "latest_version": instance.latest_version,
                "title": instance.title,
                "text": instance.text,
                "button": instance.button,
            }
        }


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["url", "link"]  # noqa: RUF012


class TermsConditionsSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = TermsConditions
        fields = ["latest_version", "title", "text", "button", "agree", "links"]  # noqa: RUF012

    def get_links(self, obj):
        serializer = LinkSerializer(Link.objects.all(), many=True, context=self.context)

        return serializer.data


class MissingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingData
        fields = ["title_android", "title_ios", "text_android", "text_ios"]  # noqa: RUF012


class AccessibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessibility
        fields = "__all__"


class GlobalRulesSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=dict(), **kwargs):  # noqa: B006
        return super(GlobalRulesSerializer, self).__init__(instance, data, **kwargs)  # noqa: PLE0101, UP008

    def to_representation(self, instance):
        serialized_terms_and_conditions = TermsConditionsSerializer(
            TermsConditions.objects.first(), many=False, context=self.context
        )

        serialized_missing_data = MissingDataSerializer(
            MissingData.objects.first(), many=False, context=self.context
        )

        serialized_app_version = AppVersionSerializer(
            AppVersion.objects.all(), many=True, context=self.context
        )

        # Flaten the list of dictionaries
        result = {}
        for line in serialized_app_version.data:
            result.update(line)

        serialized_accessibility_statements = AccessibilitySerializer(
            Accessibility.objects.all(), many=True, context=self.context
        )

        return {
            "terms_conditions": serialized_terms_and_conditions.data,
            "missing_data": serialized_missing_data.data,
            "app": result,
            "accessibility": serialized_accessibility_statements.data,
        }
