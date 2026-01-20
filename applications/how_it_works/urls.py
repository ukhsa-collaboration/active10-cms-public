from django.urls import path

from applications.how_it_works.views import HowItWorksView

urlpatterns = [
    path("", HowItWorksView.as_view(), name="how_it_works"),
]
