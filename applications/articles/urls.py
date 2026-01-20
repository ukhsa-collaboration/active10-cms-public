from django.urls import include, path
from rest_framework import routers

from .views import ArticleCategoriesViewSet, ArticlesViewSet

router = routers.SimpleRouter()
router.register(r"articles", ArticlesViewSet, basename="ArticlesViewSet")
router.register(r"categories", ArticleCategoriesViewSet, basename="ArticleCategoriesViewSet")

urlpatterns = [
    path("", include(router.urls)),
]
