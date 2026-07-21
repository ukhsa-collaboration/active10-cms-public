from rest_framework.generics import RetrieveAPIView

from applications.onboarding.serializers import OnboardingSerializer
from applications.onboarding.models import Onboarding
from utils.activity import pick_by_activity, resolve_activity


class OnboardingView(RetrieveAPIView):
    serializer_class = OnboardingSerializer

    def get_object(self):
        return pick_by_activity(Onboarding.objects.all(), resolve_activity(self.request))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["activity"] = resolve_activity(self.request)
        return context
