from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from applications.how_it_works.models import HowItWorks
from utils.admin import CloneAdminMixin


class HowItWorksAdmin(CloneAdminMixin, SortableAdminMixin, admin.ModelAdmin):
    clone_name_field = "title"
    fields = ["id", "title", "description", "image", "list_order", "activity_type"]
    readonly_fields = ["id", "list_order"]
    list_display = ["list_order", "title", "activity_type"]
    list_filter = ["activity_type"]


admin.site.register(HowItWorks, HowItWorksAdmin)
