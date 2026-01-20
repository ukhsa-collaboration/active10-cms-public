from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .docs import notifications_doc
from .serializers import GlobalRulesSerializer


@method_decorator(name="get", decorator=notifications_doc())
class GlobalRulesView(GenericAPIView):
    serializer_class = GlobalRulesSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
