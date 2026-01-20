from admin_ordering.admin import OrderableAdmin
from django.contrib import admin

from .models import View, ViewMedia, ViewProperty, ViewsRelation


class ViewMediaInline(admin.StackedInline):
    model = ViewMedia
    extra = 1


class ViewPropertyInline(admin.StackedInline):
    model = ViewProperty
    extra = 1


class ViewsRelationInline(admin.StackedInline):
    model = ViewsRelation
    extra = 1
    fk_name = "child"


class ViewChildInline(OrderableAdmin, admin.TabularInline):
    model = ViewsRelation
    extra = 0
    fk_name = "parent"
    verbose_name_plural = "View children"
    ordering = ("order",)
    ordering_field = "order"
    ordering_field_hide_input = True


class ViewArticlesInline(OrderableAdmin, admin.TabularInline):
    fields = ("article", "order")
    model = View.articles.through
    extra = 0
    fk_name = "view"
    verbose_name = "Child Article"
    ordering = ("order",)
    ordering_field = "order"
    ordering_field_hide_input = True


@admin.register(View, site=admin.site)
class ViewAdmin(admin.ModelAdmin):
    inlines = [  # noqa: RUF012
        ViewMediaInline,
        ViewPropertyInline,
        ViewsRelationInline,
        ViewChildInline,
        ViewArticlesInline,
    ]
    list_display = ("title", "type", "slug")

    fieldsets = (
        (
            "Main",
            {
                "fields": (
                    "type",
                    "slug",
                    "title",
                    "description",
                    "analytics_tag",
                    "version",
                ),
                "classes": (
                    "baton-tabs-init",
                    "baton-tab-group-fs-article--inline-articleview",
                    "baton-tab-group-fs-view_children--inline-parents",
                ),
            },
        ),
        (
            "Articles Order",
            {
                "fields": (),
                "classes": ("tab-fs-article",),
                "description": "Article children order",
            },
        ),
        (
            "View Children",
            {
                "fields": (),
                "classes": ("tab-fs-view_children",),
                "description": "View relations",
            },
        ),
    )
