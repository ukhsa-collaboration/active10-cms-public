from django.contrib import admin

from applications.tips.models import MainTip


class MainTipAdmin(admin.ModelAdmin):
    fields = ["id", "title", "description", "image"]  # noqa: RUF012
    readonly_fields = ["id"]  # noqa: RUF012


admin.site.register(MainTip, MainTipAdmin)
