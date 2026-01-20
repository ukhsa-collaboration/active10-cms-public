from rest_framework import serializers

from applications.tips.models import MainTip


class MainTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainTip
        fields = "__all__"
