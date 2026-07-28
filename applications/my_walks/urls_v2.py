from django.urls import path

from applications.my_walks.views import MyWalksV2View


urlpatterns = [
    path("", MyWalksV2View.as_view(), name="my_walks_v2"),
]
