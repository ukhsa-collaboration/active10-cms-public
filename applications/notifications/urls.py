from django.urls import path

from applications.notifications.views import NotificationsView

urlpatterns = [
    path("", NotificationsView.as_view(), name="notifications"),
]
