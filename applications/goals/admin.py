from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from applications.goals.models import Goal


@admin.register(Goal, site=admin.site)
class ArticleAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Goal
    list_display = (
        "order",
        "text",
        "user",
    )
    fieldsets = [  # noqa: RUF012
        (
            None,
            {
                "fields": [
                    "order",
                    "text",
                    "user",
                ],
            },
        ),
    ]
    readonly_fields = ("order",)
