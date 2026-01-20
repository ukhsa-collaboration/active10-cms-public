from rest_framework import viewsets

from .models import WalkingPlan
from .serializers import WalkingPlanSerializer


class WalkingPlanViewSet(viewsets.ModelViewSet):
    models = WalkingPlan
    queryset = WalkingPlan.objects.all()
    serializer_class = WalkingPlanSerializer
    http_method_names = ["get", "options"]  # noqa: RUF012
    lookup_field = "id"
