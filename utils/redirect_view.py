from django.shortcuts import redirect
from weightloss.settings import STATIC_URL


def _get_path_without_prefix(path):
    return "/".join(path.split("/")[2:])


def redirect_static_view(request):
    return redirect(f"{STATIC_URL}{_get_path_without_prefix(request.path)}")
