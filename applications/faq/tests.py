"""DB-free tests (pytest + mock). No django_db marker => DB access is blocked."""

from types import SimpleNamespace
from unittest import mock

import applications.faq.views as views
from applications.faq.models import Faq
from utils.activity import ActivityType


def test_get_queryset_applies_activity_filter():
    view = views.FaqView()
    view.request = SimpleNamespace(query_params={"activity_type": "wheeling"})
    with mock.patch.object(views, "filter_by_activity", return_value="QS") as fa:
        assert view.get_queryset() == "QS"
    assert fa.call_args.args[1] == ActivityType.WHEELING


def test_get_queryset_defaults_to_walking():
    view = views.FaqView()
    view.request = SimpleNamespace(query_params={})
    with mock.patch.object(views, "filter_by_activity", return_value="QS") as fa:
        view.get_queryset()
    assert fa.call_args.args[1] == ActivityType.WALKING


def test_str():
    assert str(Faq(title="Why walk?")) == "Why walk?"
