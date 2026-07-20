from rest_framework.generics import ListAPIView

from applications.how_it_works.serializers import HowItWorksSerializer
from applications.how_it_works.models import HowItWorks
from utils.activity import filter_by_activity, resolve_activity


class HowItWorksView(ListAPIView):
    serializer_class = HowItWorksSerializer
    queryset = HowItWorks.objects.order_by("list_order", "id")

    def get_queryset(self):
        return filter_by_activity(super().get_queryset(), resolve_activity(self.request))
