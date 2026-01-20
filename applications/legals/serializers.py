from rest_framework import serializers

from ..articles.utils.text_parser import html_text_to_json
from .models import Legal


class LegalSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField("get_content_as_json")
    shouldAccept = serializers.BooleanField(source="should_accept")
    pageType = serializers.CharField(source="page_type")

    def get_content_as_json(self, obj):
        return html_text_to_json(obj.content)

    class Meta:
        model = Legal
        fields = ["pageType", "title", "content", "shouldAccept", "version"]  # noqa: RUF012
