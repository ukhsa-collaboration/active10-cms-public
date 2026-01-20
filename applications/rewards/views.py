from rest_framework import viewsets

from applications.rewards.models import Reward
from applications.rewards.serializers import RewardSerializer


class RewardViewSet(viewsets.ModelViewSet):
    model = Reward
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    http_method_names = ["get", "head", "options"]  # noqa: RUF012
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Reward.objects.filter(
            category__in=["goalGetter", "targetChaser", "briskMinutes", "steppingUp"]
        ).order_by("position")
        category = self.request.query_params.get("category", None)

        if category:
            queryset = queryset.filter(category__iexact=category)

        return queryset


class RewardV2ViewSet(viewsets.ModelViewSet):
    model = Reward
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    http_method_names = ["get", "head", "options"]  # noqa: RUF012
    lookup_field = "slug"

    def get_queryset(self):
        slugs = [
            "goalSetter",
            "starStudent",
            "healthGuru",
            "getSetGo",
            "buddyUp",
            "fitFam",
            "moverAndShaker",
            "onTarget",
            "threeDayStreak",
            "perfectWeek",
            "twoWeekStreak",
            "perfectMonth",
            "hundredClub",
            "twoHundredFiftyClub",
            "fiveHundredClub",
            "thousandClub",
            "twoThousandClub",
            "threeThousandClub",
            "hatTrick",
            "highFive",
            "wonderWeek",
            "healthyHiker",
            "fightingFit",
            "quickMarch",
            "aimingHigh",
            "highAchiever",
            "targetChaser",
        ]
        queryset = Reward.objects.filter(slug__in=slugs).order_by("position")
        category = self.request.query_params.get("category", None)

        if category:
            queryset = queryset.filter(category__iexact=category)

        return queryset


class RewardV3ViewSet(viewsets.ModelViewSet):
    model = Reward
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    http_method_names = ["get", "head", "options"]  # noqa: RUF012
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Reward.objects.all().order_by("position")
        category = self.request.query_params.get("category", None)

        if category:
            queryset = queryset.filter(category__iexact=category)

        return queryset
