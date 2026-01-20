from rest_framework import serializers

from applications.goals.models import Goal


class GoalSerializers(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = (
            "order",
            "id",
            "text",
            "user",
        )
