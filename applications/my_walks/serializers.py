from rest_framework import serializers

from applications.my_walks.models import MyWalk, Target, TodayWalk
from applications.my_walks.utils import (
    create_my_walk_representation,
    create_target_representation,
)


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = "__all__"

    def to_representation(self, instance):
        original_representation = super(TargetSerializer, self).to_representation(instance)  # noqa: UP008
        final_representation = create_target_representation(
            original_representation.get("condition"),
            original_representation.get("text"),
        )
        return final_representation


class TodayWalkDynamicTextSerializer(serializers.ModelSerializer):
    target = TargetSerializer(many=True, source="target_set")

    class Meta:
        model = TodayWalk
        fields = "__all__"


class MyWalkDynamicTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyWalk
        fields = "__all__"


class MyWalksSerializer(serializers.Serializer):
    my_walks_dynamic_text = serializers.SerializerMethodField()
    todays_walks_dynamic_text = serializers.SerializerMethodField()

    def __init__(self, instance=None, data=dict(), **kwargs):  # noqa: B006
        return super(MyWalksSerializer, self).__init__(instance, data, **kwargs)  # noqa: PLE0101, UP008

    def get_my_walks_dynamic_text(self, obj):
        return MyWalkDynamicTextSerializer(MyWalk.objects.all(), many=True).data

    def get_todays_walks_dynamic_text(self, obj):
        return TodayWalkDynamicTextSerializer(TodayWalk.objects.all(), many=True).data

    def to_representation(self, instance):
        original_representation = super(MyWalksSerializer, self).to_representation(instance)  # noqa: UP008
        final_representation = create_my_walk_representation(original_representation)
        return final_representation
