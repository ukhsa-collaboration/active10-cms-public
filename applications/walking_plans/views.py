from django.db.models import Prefetch
from rest_framework import viewsets

from .models import PlanItineraryItem, WalkingPlan
from .serializers import WalkingPlanSerializer


class WalkingPlanViewSet(viewsets.ModelViewSet):
    models = WalkingPlan
    queryset = WalkingPlan.objects.prefetch_related(
        'sex', 'age', 'activity_level', 'motivation',
        'inferior_plans', 'superior_plans',
        Prefetch('plan_itinerary_items', queryset=PlanItineraryItem.objects.order_by('ordering')),
    ).all()
    serializer_class = WalkingPlanSerializer
    http_method_names = ["get", "options"]  # noqa: RUF012
    lookup_field = "id"
