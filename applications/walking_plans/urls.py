from django.urls import include, path
from rest_framework import routers

from .views import WalkingPlanViewSet

router = routers.SimpleRouter()
router.register(r"plans", WalkingPlanViewSet, basename="WalkingPlanViewSet")

urlpatterns = [
    path("", include(router.urls)),
]
