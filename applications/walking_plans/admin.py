from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from .models import ActivityLevel, Age, PlanItineraryItem, Sex, WalkingPlan


class PlanItineraryItemInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()

        for form in self.forms:
            if len(form.cleaned_data.keys()) == 0:
                continue

            if len(form.cleaned_data.get("daily_brisk_minutes")) != 7:  # noqa: PLR2004
                form.errors["daily_brisk_minutes"] = form.error_class(
                    ["Daily brisk minutes must have 7 values."]
                )

            if sum(form.cleaned_data.get("daily_brisk_minutes")) != form.cleaned_data.get(
                "total_brisk_minutes"
            ):
                form.errors["daily_brisk_minutes"] = form.error_class(
                    ["Daily brisk minutes must sum to total brisk minutes."]
                )

            if len(form.cleaned_data.get("daily_non_brisk_minutes")) != 7:  # noqa: PLR2004
                form.errors["daily_non_brisk_minutes"] = form.error_class(
                    ["Daily non-brisk minutes must have 7 values."]
                )

            if sum(form.cleaned_data.get("daily_non_brisk_minutes")) != form.cleaned_data.get(
                "total_non_brisk_minutes"
            ):
                form.errors["daily_non_brisk_minutes"] = form.error_class(
                    ["Daily non-brisk minutes must sum to total non-brisk minutes."]
                )


class PlanItineraryItemInline(admin.TabularInline):
    model = PlanItineraryItem
    extra = 1
    formset = PlanItineraryItemInlineFormset


@admin.register(WalkingPlan, site=admin.site)
class WalkingPlanAdmin(admin.ModelAdmin):
    list_display = (
        "plan_name",
        "plan_code",
        "plan_tagline",
        "plan_duration",
        "plan_brisk_minutes_per_day",
        "plan_goal",
    )
    inlines = [PlanItineraryItemInline]  # noqa: RUF012


@admin.register(Age, site=admin.site)
class AgeAdmin(admin.ModelAdmin):
    list_display = ("label",)


@admin.register(Sex, site=admin.site)
class SexAdmin(admin.ModelAdmin):
    list_display = ("label",)


@admin.register(ActivityLevel, site=admin.site)
class ActivityLevelAdmin(admin.ModelAdmin):
    list_display = ("label",)
