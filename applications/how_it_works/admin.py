from django.contrib import admin
from applications.how_it_works.models import HowItWorks
from utils.admin import CloneAdminMixin


class HowItWorksAdmin(CloneAdminMixin, admin.ModelAdmin):
    clone_name_field = "title"
    fields = ["id", "title", "description", "image", "activity_type"]
    readonly_fields = ["id"]
    list_display = ["title", "activity_type"]
    list_filter = ["activity_type"]


admin.site.register(HowItWorks, HowItWorksAdmin)
