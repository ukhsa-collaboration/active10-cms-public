from django.urls import path

from applications.goals.views import GoalsView

urlpatterns = [
    path("", GoalsView.as_view(), name="goals"),
]
