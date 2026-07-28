from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from applications.tips.models import MainTip
from utils.admin import CloneAdminMixin


class MainTipAdmin(CloneAdminMixin, SortableAdminMixin, admin.ModelAdmin):
    clone_name_field = "title"
    fields = ["id", "title", "description", "image", "list_order", "activity_type"]
    readonly_fields = ["id", "list_order"]
    list_display = ["list_order", "title", "activity_type", "published"]
    list_filter = ["activity_type", "published"]


admin.site.register(MainTip, MainTipAdmin)
