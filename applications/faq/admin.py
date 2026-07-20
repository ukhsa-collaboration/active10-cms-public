from django.contrib import admin
from applications.faq.models import Faq
from utils.admin import CloneAdminMixin


class FaqAdmin(CloneAdminMixin, admin.ModelAdmin):
    clone_name_field = "title"
    fields = ["id", "title", "text", "list_order", "activity_type"]
    readonly_fields = ["id", ]
    list_display = ["title", "activity_type"]
    list_filter = ["activity_type"]


admin.site.register(Faq, FaqAdmin)
