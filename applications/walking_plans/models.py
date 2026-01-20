from admin_ordering.models import OrderableModel
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Sex(models.Model):
    label = models.CharField(max_length=32, default="", blank=True)

    def __str__(self):
        return self.label


class Age(models.Model):
    label = models.CharField(max_length=32, default="", blank=True)

    def __str__(self):
        return self.label


class ActivityLevel(models.Model):
    label = models.CharField(max_length=32, default="", blank=True)

    def __str__(self):
        return self.label


class WalkingPlan(models.Model):
    image = models.ImageField(upload_to="walking_plans/", blank=True, null=True)
    plan_name = models.CharField(max_length=256, blank=True, default="")
    plan_code = models.CharField(max_length=256, blank=True, default="")
    plan_tagline = models.CharField(max_length=256, blank=True, default="")
    plan_description = models.TextField(blank=True, default="")
    plan_full_description = models.TextField(blank=True, default="")
    plan_duration = models.CharField(max_length=256, blank=True, default="")
    plan_duration_weeks = models.PositiveIntegerField(default=0)
    plan_brisk_minutes_per_day = models.CharField(max_length=128, blank=True, default="")
    plan_goal = models.TextField(blank=True, default="")
    plan_difficulty = models.CharField(max_length=32, blank=True, default="")
    reward = models.ForeignKey("rewards.Reward", on_delete=models.CASCADE, null=True, blank=True)

    superior_plan = models.ForeignKey(
        "walking_plans.WalkingPlan",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="inferior_plans",
    )
    inferior_plan = models.ForeignKey(
        "walking_plans.WalkingPlan",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="superior_plans",
    )

    age = models.ManyToManyField(Age, blank=True)
    sex = models.ManyToManyField(Sex, blank=True)
    motivation = models.ManyToManyField("goals.Goal", blank=True)
    activity_level = models.ManyToManyField(ActivityLevel, blank=True)

    def __str__(self):
        return self.plan_name


class PlanItineraryItem(OrderableModel):
    week_label = models.CharField(max_length=128, blank=True, default="")
    description_of_weekly_task = models.TextField(blank=True, default="")
    total_brisk_minutes = models.PositiveIntegerField(default=0)
    daily_brisk_minutes = ArrayField(models.PositiveIntegerField(), default=list, size=7)
    total_non_brisk_minutes = models.PositiveIntegerField(default=0)
    daily_non_brisk_minutes = ArrayField(models.PositiveIntegerField(), default=list, size=7)
    walking_plan = models.ForeignKey(
        WalkingPlan,
        on_delete=models.CASCADE,
        null=True,
        related_name="plan_itinerary_items",
    )
