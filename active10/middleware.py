from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.html import strip_tags

from active10.settings import APP_ENV


class Enforce2FA:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (  # noqa: SIM102
            request.user.is_authenticated
            and not request.user.is_verified()
            and APP_ENV != "development"
        ):
            if (
                "dhsc-admin" in request.path
                and "logout" not in request.path
                and "two_factor" not in request.path
            ):
                return redirect("two_factor:setup")

        response = self.get_response(request)
        return response


class AdminSanitizationMiddleware(MiddlewareMixin):
    def __call__(self, request):
        if request.path.startswith("/dhsc-admin/auth/user/") and request.method == "POST":
            request.POST = request.POST.copy()
            for key, value in request.POST.items():
                request.POST[key] = strip_tags(value)

        return self.get_response(request)


class RemoveServerHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # if "Server" in response.headers:
        #     del response.headers["Server"]
        response.__setitem__("Server", "active10app")
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # these headers do not necessarily apply to this app
        # response['Cross-Origin-Embedder-Policy'] = 'require-corp'
        # response['Cross-Origin-Resource-Policy'] = 'same-origin'
        return response


class HostValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = ["/healthcheck"]
        allowed_hosts = [
            "active10.dev.phedigital.co.ukactive10.stg.phedigital.co.uk",
            "active10.prod.phedigital.co.uk",
            "cms.phedigital.co.uk",
        ]
        if settings.APP_ENV != "development" and (
            request.path not in allowed_paths and request.get_host() not in allowed_hosts
        ):
            raise SuspiciousOperation("Invalid Host header")
        return self.get_response(request)
