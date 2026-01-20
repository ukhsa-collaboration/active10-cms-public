from django.contrib import admin

from .models import Legal


class LegalAdmin(admin.ModelAdmin):
    list_display = ("title", "public", "should_accept", "version")


admin.site.register(Legal, LegalAdmin)
