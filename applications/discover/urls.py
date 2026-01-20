from django.urls import path

from applications.discover.views import DiscoverView

urlpatterns = [
    path("", DiscoverView.as_view(), name="discover"),
]
