from rest_framework import serializers

from .models import View, ViewMedia, ViewProperty


class ViewMediaSerializer(serializers.ModelSerializer):
    resourceId = serializers.CharField(source="resource_id")

    class Meta:
        model = ViewMedia
        fields = ["type", "tag", "id", "resourceId", "label", "url"]  # noqa: RUF012


class ViewPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewProperty
        fields = ["key", "value"]  # noqa: RUF012


class ViewSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()
    article_ids = serializers.SerializerMethodField()
    children_ids = serializers.SerializerMethodField()
    analyticsTag = serializers.CharField(source="analytics_tag", allow_null=True, allow_blank=True)
    version = serializers.IntegerField(default=0)

    class Meta:
        model = View
        fields = [  # noqa: RUF012
            "id",
            "type",
            "slug",
            "title",
            "description",
            "analyticsTag",
            "version",
            "properties",
            "media",
            "children_ids",
            "article_ids",
        ]
        lookup_field = "slug"

    def get_children_ids(self, obj):
        return [r.child_id for r in obj.parents.all()]

    def get_article_ids(self, obj):
        return [av.article_id for av in obj.articleview_set.all()]

    def get_media(self, obj):
        return ViewMediaSerializer(
            obj.view_media.all(),many=True,context=self.context
        ).data

    def get_properties(self, obj):
        return ViewPropertySerializer(
            obj.view_property.all(),many=True,context=self.context
        ).data
