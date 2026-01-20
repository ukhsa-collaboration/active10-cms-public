from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .docs import my_walk_doc
from .serializers import MyWalksSerializer


@method_decorator(name="get", decorator=my_walk_doc())
class MyWalksView(GenericAPIView):
    serializer_class = MyWalksSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
