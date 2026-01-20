from rest_framework import serializers

from .models import PlanItineraryItem, WalkingPlan


class PlanItineraryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanItineraryItem
        fields = (
            "id",
            "week_label",
            "description_of_weekly_task",
            "total_brisk_minutes",
            "daily_brisk_minutes",
            "total_non_brisk_minutes",
            "daily_non_brisk_minutes",
        )


class WalkingPlanSerializer(serializers.ModelSerializer):
    plan_itinerary_items = serializers.SerializerMethodField()
    category_details = serializers.SerializerMethodField()
    inferior_plan_ids = serializers.SerializerMethodField()
    superior_plan_ids = serializers.SerializerMethodField()

    class Meta:
        model = WalkingPlan
        fields = (
            "id",
            "image",
            "plan_name",
            "plan_code",
            "plan_tagline",
            "plan_description",
            "plan_duration",
            "plan_duration_weeks",
            "plan_brisk_minutes_per_day",
            "plan_goal",
            "plan_difficulty",
            "plan_itinerary_items",
            "category_details",
            "inferior_plan_ids",
            "superior_plan_ids",
        )

    def get_category_details(self, obj):
        result = {
            "sex": obj.sex.values_list("label", flat=True),
            "age": obj.age.values_list("label", flat=True),
            "activity_level": obj.activity_level.values_list("label", flat=True),
            "motivation": obj.motivation.values_list("text", flat=True),
        }

        return result

    def get_inferior_plan_ids(self, obj):
        return obj.inferior_plans.values_list("id", flat=True)

    def get_superior_plan_ids(self, obj):
        return obj.superior_plans.values_list("id", flat=True)

    def get_plan_itinerary_items(self, obj):
        return PlanItineraryItemSerializer(
            obj.plan_itinerary_items.order_by("ordering"), many=True
        ).data
