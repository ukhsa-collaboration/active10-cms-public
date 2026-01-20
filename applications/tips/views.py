from django.db.models import Q
from rest_framework.generics import ListAPIView

from applications.tips.models import MainTip
from applications.tips.serializers import MainTipSerializer


class TipsView(ListAPIView):
    serializer_class = MainTipSerializer
    queryset = MainTip.objects.filter(Q(published=True)).order_by("list_order", "id")
