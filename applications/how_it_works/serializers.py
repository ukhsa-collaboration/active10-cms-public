from rest_framework import serializers

from applications.how_it_works.models import HowItWorks


class HowItWorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowItWorks
        fields = "__all__"
