from rest_framework import serializers

from applications.faq.models import Faq


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ["id", "title", "text"]  # noqa: RUF012
