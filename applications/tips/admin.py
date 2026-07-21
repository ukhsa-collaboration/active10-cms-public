from django.contrib import admin
from applications.tips.models import MainTip
from utils.admin import CloneAdminMixin


class MainTipAdmin(CloneAdminMixin, admin.ModelAdmin):
    clone_name_field = "title"
    fields = ["id", "title", "description", "image", "activity_type"]
    readonly_fields = ["id"]
    list_display = ["title", "activity_type", "published"]
    list_filter = ["activity_type", "published"]


admin.site.register(MainTip, MainTipAdmin)
