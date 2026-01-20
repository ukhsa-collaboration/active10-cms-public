from django.urls import path

from applications.about_one_you.views import AboutOneYouView

urlpatterns = [
    path("", AboutOneYouView.as_view(), name="about_one_you"),
]
