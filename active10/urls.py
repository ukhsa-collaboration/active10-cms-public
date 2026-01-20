"""active10 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from baton.autodiscover import admin
from baton.views import GetAppListJsonView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import authentication, permissions
from two_factor.urls import urlpatterns as tf_urls

from applications.versions.views import IntegrityTokenView, check_integrity_token


def _get_app_list_json(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    return GetAppListJsonView().get(request)


def _get_path_without_prefix(path):
    return "/".join(path.split("/")[2:])


def redirect_static_view(request):
    return redirect(f"{settings.STATIC_URL}{_get_path_without_prefix(request.path)}")


schema_view = get_schema_view(
    openapi.Info(
        title="Active10 API docs",
        default_version="v1",
        description="Active10 CMS",
    ),
    public=False,
    permission_classes=(permissions.IsAdminUser,),
    authentication_classes=(authentication.SessionAuthentication,),
)


urlpatterns = [
    path("baton/app-list-json/", _get_app_list_json),
    path("", include(tf_urls)),
    path("dhsc-admin/", admin.site.urls),
    path("baton/", include("baton.urls")),
    path("admin/versions/", include("applications.versions.urls")),
    path("api/v1/active10/about-one-you/", include("applications.about_one_you.urls")),
    path("api/v1/active10/faq/", include("applications.faq.urls")),
    path("api/v1/active10/discover/", include("applications.discover.urls")),
    path("api/v1/active10/dynamic-texts/", include("applications.my_walks.urls")),
    path("api/v1/active10/onboarding/", include("applications.onboarding.urls")),
    path("api/v1/active10/goals/", include("applications.goals.urls")),
    path("api/v1/active10/tips/", include("applications.tips.urls")),
    path("api/v1/active10/how-it-works/", include("applications.how_it_works.urls")),
    path("api/v1/active10/notifications/", include("applications.notifications.urls")),
    path("api/v1/active10/global_rules/", include("applications.global_rules.urls")),
    path("api/v1/active10/legals/", include("applications.legals.urls")),
    path("api/", include("applications.rewards.urls")),
    path(
        "api/v1/active10/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/v1/active10/", include("applications.articles.urls")),
    path("api/v1/active10/", include("applications.views.urls")),
    path(
        "api/v1/check-integrity-token",
        check_integrity_token,
        name="check-integrity-token",
    ),
    path(
        "api/v1/new-check-integrity-token",
        IntegrityTokenView.as_view(),
        name="new-check-integrity-token",
    ),
    path("api/v1/active10/walking-plans/", include("applications.walking_plans.urls")),
    re_path(r"^static/*", redirect_static_view),
    re_path("healthcheck", include("health_check.urls")),
    re_path(r"^favicon\.ico$", RedirectView.as_view(url=f"{settings.STATIC_URL}favicon.ico")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
