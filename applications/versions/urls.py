from django.urls import path

from .views import revert_view

urlpatterns = [
    path("revert/<int:id>/", revert_view, name="revert-view"),
]
