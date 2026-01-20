from rest_framework.generics import ListAPIView

from applications.faq.models import Faq
from applications.faq.serializers import FaqSerializer


class FaqView(ListAPIView):
    serializer_class = FaqSerializer
    queryset = Faq.objects.order_by("list_order", "id")
