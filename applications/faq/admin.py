from django.contrib import admin

from applications.faq.models import Faq


class FaqAdmin(admin.ModelAdmin):
    fields = ["id", "title", "text", "list_order"]  # noqa: RUF012
    readonly_fields = [  # noqa: RUF012
        "id",
    ]


admin.site.register(Faq, FaqAdmin)
