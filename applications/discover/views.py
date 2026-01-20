from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .docs import discover_doc
from .models import Carousel, Discover
from .serializers import DiscoverSerializer, TipSerializer


@method_decorator(name="get", decorator=discover_doc())
class DiscoverView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        discover_serializer = DiscoverSerializer(
            Discover.objects.filter(published=True),
            many=True,
            context=self.get_serializer_context(),
        )
        tip_serializer = TipSerializer(
            Carousel.objects.filter(published=True),
            many=True,
            context=self.get_serializer_context(),
        )
        return Response(dict(discover=discover_serializer.data, tips=tip_serializer.data))
