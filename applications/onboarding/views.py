from rest_framework.generics import RetrieveAPIView

from applications.onboarding.models import Onboarding
from applications.onboarding.serializers import OnboardingSerializer


class OnboardingView(RetrieveAPIView):
    serializer_class = OnboardingSerializer

    def get_object(self):
        return Onboarding.objects.first()
