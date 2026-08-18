from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportMixin, ExportActionMixin
from utils.admin import CloneAdminMixin
from .models import (
    Article,
    ArticleCategory,
    ArticleRelated,
    ArticleView,
    ContentView,
    Image,
)


class ArticleRelatedInline(admin.TabularInline):
    model = ArticleRelated
    fk_name = "article"
    extra = 1


class ArticleViewInline(admin.TabularInline):
    model = ArticleView
    extra = 1


class ContentViewsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ContentView
    extra = 1
    ordering = ("order",)


class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article


@admin.register(Article, site=admin.site)
class ArticleAdmin(CloneAdminMixin, SortableAdminBase, admin.ModelAdmin):
    # resource_class = ArticleResource
    clone_name_field = "title"
    model = Article
    inlines = [ArticleViewInline, ArticleRelatedInline, ContentViewsInline]  # noqa: RUF012
    list_display = ("title", "type", "description", "get_parent_views", "published", "activity_type")
    search_fields = (
        "title",
        "type",
        "slug",
        "views__slug",
        "views__title",
        "views__type",
    )
    list_filter = ("published", "type", "user_group", "activity_type")
    list_per_page = 10

    def after_save_clone(self, original, clone):
        # Re-create the relationship rows, reusing the same shared targets.
        for article_view in ArticleView.objects.filter(article=original):
            ArticleView.objects.create(article=clone, view=article_view.view, order=article_view.order)
        for related in ArticleRelated.objects.filter(article=original):
            ArticleRelated.objects.create(
                article=clone, related_article=related.related_article, order=related.order
            )
        for content_view in ContentView.objects.filter(article=original):
            ContentView.objects.create(article=clone, view=content_view.view, order=content_view.order)


@admin.register(Image, site=admin.site)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("name", "image_tag",)
    search_fields = ("name",)
    list_per_page = 10


@admin.register(ArticleCategory, site=admin.site)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_per_page = 10
