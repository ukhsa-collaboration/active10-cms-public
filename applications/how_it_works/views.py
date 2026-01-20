from rest_framework.generics import ListAPIView

from applications.how_it_works.models import HowItWorks
from applications.how_it_works.serializers import HowItWorksSerializer


class HowItWorksView(ListAPIView):
    serializer_class = HowItWorksSerializer
    queryset = HowItWorks.objects.order_by("list_order", "id")
