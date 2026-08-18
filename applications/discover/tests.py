"""DB-free tests (pytest + mock). No django_db marker => DB access is blocked."""

from types import SimpleNamespace
from unittest import mock

import applications.discover.views as views
from utils.activity import ActivityType


def test_get_filters_discover_tiles_by_activity():
    view = views.DiscoverView()
    request = SimpleNamespace(query_params={"activity_type": "wheeling"})
    view.request = request
    view.format_kwarg = None
    with (
        mock.patch.object(views, "filter_by_activity", return_value=mock.MagicMock()) as fa,
        mock.patch.object(views, "DiscoverSerializer", return_value=SimpleNamespace(data=[{"description": "x"}])),
        mock.patch.object(views, "TipSerializer", return_value=SimpleNamespace(data=[])),
    ):
        response = view.get(request)
    assert response.data == {"discover": [{"description": "x"}], "tips": []}
    assert fa.call_args.args[1] == ActivityType.WHEELING


def test_get_defaults_to_walking():
    view = views.DiscoverView()
    request = SimpleNamespace(query_params={})
    view.request = request
    view.format_kwarg = None
    with (
        mock.patch.object(views, "filter_by_activity", return_value=mock.MagicMock()) as fa,
        mock.patch.object(views, "DiscoverSerializer", return_value=SimpleNamespace(data=[])),
        mock.patch.object(views, "TipSerializer", return_value=SimpleNamespace(data=[])),
    ):
        view.get(request)
    assert fa.call_args.args[1] == ActivityType.WALKING
