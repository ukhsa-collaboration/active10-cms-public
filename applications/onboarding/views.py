from rest_framework.generics import ListAPIView, RetrieveAPIView

from applications.onboarding.models import Onboarding
from applications.onboarding.serializers import OnboardingSerializer, OnboardingSerializerV2
from utils.activity import filter_by_activity, pick_by_activity, resolve_activity


class OnboardingView(RetrieveAPIView):
    serializer_class = OnboardingSerializer

    def get_object(self):
        onboarding_obj = pick_by_activity(Onboarding.objects.all(), resolve_activity(self.request))
        if onboarding_obj:
            return onboarding_obj
        raise self.get_object().DoesNotExist("No onboarding object found for the requested activity type.")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["activity"] = resolve_activity(self.request)
        return context


class OnboardingV2View(ListAPIView):
    """Onboarding copy for every activity type the request asks for.

    Where v1 serves the single best-matching record, v2 serves the cascade as a
    list — walking + both, wheeling + both, or the full catalogue for
    ``?activity_type=both``.
    """

    serializer_class = OnboardingSerializerV2
    queryset = Onboarding.objects.order_by("activity_type", "id")

    def get_queryset(self):
        return filter_by_activity(super().get_queryset(), resolve_activity(self.request))
