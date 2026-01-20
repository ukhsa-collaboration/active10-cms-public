from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from import_export import resources

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
class ArticleAdmin(SortableAdminBase, admin.ModelAdmin):
    # resource_class = ArticleResource
    model = Article
    inlines = [ArticleViewInline, ArticleRelatedInline, ContentViewsInline]  # noqa: RUF012
    list_display = ("title", "type", "description", "get_parent_views", "published")
    search_fields = (
        "title",
        "type",
        "slug",
        "views__slug",
        "views__title",
        "views__type",
    )
    list_filter = ("published", "type", "user_group")
    list_per_page = 10


@admin.register(Image, site=admin.site)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "image_tag",
    )
    search_fields = ("name",)
    list_per_page = 10


@admin.register(ArticleCategory, site=admin.site)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_per_page = 10
