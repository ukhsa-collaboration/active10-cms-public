from django.urls import include, path
from rest_framework import routers

from .views import RemakeViewSet, ViewsViewSet

router = routers.SimpleRouter()
router.register(r"", ViewsViewSet, basename="ViewsViewSet")
remake_router = routers.SimpleRouter()
remake_router.register(r"", RemakeViewSet, basename="RemakeViewSet")

urlpatterns = [
    path("views", include(router.urls)),
    path("remake-view", include(remake_router.urls)),
]
