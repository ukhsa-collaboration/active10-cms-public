from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets

from .models import Legal
from .serializers import LegalSerializer


@method_decorator(cache_page(60), name="dispatch")
class LegalViewSet(viewsets.ModelViewSet):
    models = Legal
    queryset = Legal.objects.filter(public=True)
    serializer_class = LegalSerializer
    http_method_names = ["get", "head", "options"]  # noqa: RUF012
    lookup_field = "id"
