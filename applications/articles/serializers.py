from rest_framework import serializers

from .models import Article, ArticleCategory, ContentView
from .utils import html_text_to_json


class ArticleSerializer(serializers.ModelSerializer):
    relatedSectionTitle = serializers.CharField(source="related_section_title")
    relatedSectionDescription = serializers.CharField(source="related_section_description")
    analyticsTag = serializers.CharField(source="analytics_tag")
    buttonTitle = serializers.CharField(source="button_title")
    buttonAnalyticsTag = serializers.CharField(source="button_analytics_tag")
    buttonUrl = serializers.CharField(source="button_url")
    buttonAccessibilityLabel = serializers.CharField(source="button_accessibility_label")
    destination = serializers.SerializerMethodField("get_destination")
    imageUrl = serializers.SerializerMethodField("get_image_url")
    categoryId = serializers.IntegerField(source="category_id")
    categoryLabel = serializers.SerializerMethodField("get_category_name")
    categoryPosition = serializers.SerializerMethodField("get_category_position")
    content = serializers.SerializerMethodField("get_content_as_json")
    relatedArticles = serializers.SerializerMethodField("get_related_article_ids")
    view_ids = serializers.SerializerMethodField()
    content_view_ids = serializers.SerializerMethodField("get_content_view_ids")

    def get_destination(self, obj):
        android = obj.destination_android
        ios = obj.destination_ios
        return {"ios": ios, "android": android}

    def get_view_ids(self, obj):
        return obj.views.through.objects.filter(article=obj.id).order_by("order").values_list("view_id", flat=True)

    def get_related_article_ids(self, obj):
        return (
            obj.related.through.objects.filter(article=obj.id)
            .order_by("order")
            .values_list("related_article", flat=True)
        )

    def get_category_name(self, obj):
        return obj.category.name

    def get_category_position(self, obj):
        return obj.category.position

    def get_image_url(self, obj):
        return obj.image.image.url if bool(obj.image) else ""

    def get_content_as_json(self, obj):
        return html_text_to_json(obj.content)

    def get_content_view_ids(self, obj):
        return ContentView.objects.filter(article__id=obj.id).order_by("order").values_list("view_id", flat=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "slug",
            "published",
            "title",
            "description",
            "type",
            "destination",
            "destination",
            "content",
            "category",
            "analyticsTag",
            "platform",
            "imageUrl",
            "buttonTitle",
            "buttonAnalyticsTag",
            "buttonUrl",
            "buttonAccessibilityLabel",
            "categoryId",
            "categoryLabel",
            "categoryPosition",
            "relatedSectionTitle",
            "relatedSectionDescription",
            "relatedArticles",
            "view_ids",
            "content_view_ids",
            "user_group",
        ]


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ["id", "name", "position"]
