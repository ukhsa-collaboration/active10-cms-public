from django.urls import path

from applications.my_walks.views import MyWalksView

urlpatterns = [
    path("", MyWalksView.as_view(), name="my_walks"),
]
