from rest_framework import serializers

from applications.discover.models import Carousel, Cta, Discover, SplashScreen


class SplashScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SplashScreen
        fields = "__all__"


class DiscoverSerializer(serializers.ModelSerializer):
    splash_screen = SplashScreenSerializer()

    class Meta:
        model = Discover
        fields = "__all__"


class CtaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cta
        fields = "__all__"


class TipSerializer(serializers.ModelSerializer):
    cta = CtaSerializer()

    class Meta:
        model = Carousel
        fields = "__all__"
