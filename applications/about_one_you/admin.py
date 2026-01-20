from django.contrib import admin

from applications.about_one_you.models import AboutOneYou, Application


class AboutOneYouAdmin(admin.ModelAdmin):
    fields = ["id", "text"]  # noqa: RUF012
    readonly_fields = ["id"]  # noqa: RUF012


class ApplicationAdmin(admin.ModelAdmin):
    fields = ["id", "name", "description", "ios", "android", "icon", "list_order"]  # noqa: RUF012
    readonly_fields = ["id"]  # noqa: RUF012


admin.site.register(AboutOneYou, AboutOneYouAdmin)
admin.site.register(Application, ApplicationAdmin)
