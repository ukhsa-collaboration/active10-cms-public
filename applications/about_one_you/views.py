from django.utils.decorators import method_decorator
from rest_framework.generics import RetrieveAPIView

from .docs import about_on_you_doc
from .models import AboutOneYou
from .serializers import AboutOneYouSerializer


@method_decorator(name="get", decorator=about_on_you_doc())
class AboutOneYouView(RetrieveAPIView):
    serializer_class = AboutOneYouSerializer

    def get_object(self):
        return AboutOneYou.objects.first()
