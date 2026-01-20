from django.urls import path

from applications.faq.views import FaqView

urlpatterns = [
    path("", FaqView.as_view(), name="faq"),
]
