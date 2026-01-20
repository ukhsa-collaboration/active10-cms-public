from django.urls import path

from applications.global_rules.views import GlobalRulesView

urlpatterns = [
    path("", GlobalRulesView.as_view(), name="global_rules"),
]
