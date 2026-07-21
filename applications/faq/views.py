from rest_framework.generics import ListAPIView

from applications.faq.serializers import FaqSerializer
from applications.faq.models import Faq
from utils.activity import filter_by_activity, resolve_activity


class FaqView(ListAPIView):
    serializer_class = FaqSerializer
    queryset = Faq.objects.order_by("list_order", "id")

    def get_queryset(self):
        return filter_by_activity(super().get_queryset(), resolve_activity(self.request))
