from django.contrib import admin

from applications.my_walks.models import MyWalk, Target, TodayWalk


class NonEditableField:
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("condition",)  # noqa: RUF005
        return self.readonly_fields


class TargetInlineAdmin(admin.StackedInline):
    model = Target
    fields = ("condition", "text")
    can_delete = True
    extra = 0


class TodayWalkAdmin(admin.ModelAdmin):
    inlines = [TargetInlineAdmin]  # noqa: RUF012


class MyWalkAdmin(NonEditableField, admin.ModelAdmin):
    fields = ("condition", "text")


admin.site.register(TodayWalk, TodayWalkAdmin)
admin.site.register(MyWalk, MyWalkAdmin)
