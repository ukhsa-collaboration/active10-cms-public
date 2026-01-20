from django.urls import include, path
from rest_framework import routers

from applications.legals.views import LegalViewSet

router = routers.SimpleRouter()
router.register(r"", LegalViewSet, basename="LegalViewSet")

urlpatterns = [
    path("", include(router.urls)),
]
