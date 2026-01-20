from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Article, ArticleCategory
from .serializers import ArticleCategorySerializer, ArticleSerializer


@method_decorator(cache_page(60), name="dispatch")
class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(published=True)
    serializer_class = ArticleSerializer
    http_method_names = ["get", "options"]  # noqa: RUF012
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_group = request.query_params.get("user_group", "users")
        if user_group not in ["all_users", "nhs_users", "users"]:
            return Response({"error": "Invalid user group"}, status=400)

        if user_group != "all_users":
            queryset = queryset.filter(user_group__in=[user_group, "all_users"])
        else:
            queryset = queryset.filter(user_group=user_group)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@method_decorator(cache_page(60), name="dispatch")
class ArticleCategoriesViewSet(viewsets.ModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer
    http_method_names = ["get", "options"]  # noqa: RUF012
    lookup_field = "id"
