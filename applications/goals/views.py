from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework.generics import ListCreateAPIView

from .docs import goals_doc
from .models import Goal
from .serializers import GoalSerializers


@method_decorator(name="get", decorator=goals_doc())
class GoalsView(ListCreateAPIView):
    serializer_class = GoalSerializers

    def get_queryset(self):
        user = self.request.query_params.get("user")
        if user:
            queryset = Goal.objects.filter(Q(user=user) | Q(user__isnull=True)).order_by(
                "id", "user"
            )
        else:
            queryset = Goal.objects.filter(user__isnull=True).order_by("order")
        return queryset
