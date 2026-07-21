from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .docs import discover_doc
from .models import Carousel, Discover
from .serializers import DiscoverSerializer, TipSerializer
from utils.activity import filter_by_activity, resolve_activity


@method_decorator(name="get", decorator=discover_doc())
class DiscoverView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        discover_queryset = filter_by_activity(
            Discover.objects.filter(published=True).select_related("splash_screen"),
            resolve_activity(request),
        )
        discover_serializer = DiscoverSerializer(discover_queryset, many=True, context=self.get_serializer_context())
        tip_serializer = TipSerializer(Carousel.objects.filter(published=True).select_related('cta'), many=True, context=self.get_serializer_context())
        return Response(dict(discover=discover_serializer.data, tips=tip_serializer.data))
