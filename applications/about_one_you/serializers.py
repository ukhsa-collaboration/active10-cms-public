from rest_framework import serializers

from applications.about_one_you.models import AboutOneYou, Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"


class AboutOneYouSerializer(serializers.ModelSerializer):
    about = serializers.SerializerMethodField()
    apps = serializers.SerializerMethodField()

    class Meta:
        model = AboutOneYou
        fields = ["about", "apps"]  # noqa: RUF012

    def get_about(self, obj):
        return dict(text=obj.text)

    def get_apps(self, obj):
        serializer = ApplicationSerializer(
            Application.objects.all(), many=True, context=self.context
        )
        return serializer.data
