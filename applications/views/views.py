from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from utils.converter import convert

from .models import View, ViewMedia, ViewProperty
from .serializers import ViewSerializer


@method_decorator(cache_page(60), name="dispatch")
class ViewsViewSet(viewsets.ModelViewSet):
    models = View
    queryset = View.objects.all()
    serializer_class = ViewSerializer
    http_method_names = ["get", "head", "options"]  # noqa: RUF012
    lookup_field = "id"


class RemakeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ViewSerializer
    models = View

    def create(self, request, *args, **kwargs):
        for item in request.data:
            data = convert(item)

            if View.objects.filter(type="popup", slug=data["slug"]).count() != 0:
                continue

            serializer = ViewSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                created_view = serializer.instance
            else:
                return Response(serializer.errors, 404)

            for properties in data["properties"]:
                properties_obj = ViewProperty.objects.create(
                    key=properties["key"], value=properties["value"], view=created_view
                )
                properties_obj.save()

            for image in data["media"]:
                image_obj = ViewMedia.import_from_json(image, created_view)
                image_obj.save()

        return Response({"message": "success"}, 200)

    def list(self, request, *args, **kwargs):
        return Response(convert(request.data), 200)
