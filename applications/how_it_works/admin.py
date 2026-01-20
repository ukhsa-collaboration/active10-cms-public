from django.contrib import admin

from applications.how_it_works.models import HowItWorks


class HowItWorksAdmin(admin.ModelAdmin):
    fields = ["id", "title", "description", "image"]  # noqa: RUF012
    readonly_fields = ["id"]  # noqa: RUF012


admin.site.register(HowItWorks, HowItWorksAdmin)
