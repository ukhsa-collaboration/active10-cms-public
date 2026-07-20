from django.db.models import Q
from rest_framework.generics import ListAPIView

from applications.tips.models import MainTip
from applications.tips.serializers import MainTipSerializer
from utils.activity import filter_by_activity, resolve_activity


class TipsView(ListAPIView):
    serializer_class = MainTipSerializer
    queryset = MainTip.objects.filter(Q(published=True)).order_by("list_order", "id")

    def get_queryset(self):
        return filter_by_activity(super().get_queryset(), resolve_activity(self.request))
