from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from applications.goals.models import Goal
from utils.admin import CloneAdminMixin


@admin.register(Goal, site=admin.site)
class ArticleAdmin(CloneAdminMixin, SortableAdminMixin, admin.ModelAdmin):
    clone_name_field = "text"
    model = Goal
    list_display = (
        "order",
        "text",
        "user",
        "activity_type",
    )
    list_filter = ("activity_type",)
    fieldsets = [  # noqa: RUF012
        (
            None,
            {
                "fields": [
                    "order",
                    "text",
                    "user",
                    "activity_type",
                ],
            },
        ),
    ]
    readonly_fields = ("order", )
