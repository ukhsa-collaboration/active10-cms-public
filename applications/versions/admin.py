from django.contrib import admin

from .models import VersionsSet


class VersionsSetAdmin(admin.ModelAdmin):
    fields = ["name"]  # noqa: RUF012
    change_form_template = "custom_change_form.html"


admin.site.register(VersionsSet, VersionsSetAdmin)
