from django.urls import include, path
from rest_framework import routers

from applications.rewards.views import RewardV2ViewSet, RewardV3ViewSet, RewardViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"v1/active10/rewards/", RewardViewSet, basename="rewards")
router.register(r"v2/active10/rewards/", RewardV2ViewSet, basename="rewards-v2")
router.register(r"v3/active10/rewards/", RewardV3ViewSet, basename="rewards-v3")

urlpatterns = [path("", include(router.urls))]
