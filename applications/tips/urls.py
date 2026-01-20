from django.urls import path

from applications.tips.views import TipsView

urlpatterns = [
    path("", TipsView.as_view(), name="tips"),
]
