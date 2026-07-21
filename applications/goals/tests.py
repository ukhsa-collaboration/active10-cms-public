"""DB-free tests (pytest + mock). No django_db marker => DB access is blocked."""

from types import SimpleNamespace
from unittest import mock

import applications.goals.views as views
from applications.goals.models import Goal
from utils.activity import ActivityType


def test_get_queryset_global_defaults_to_walking():
    view = views.GoalsView()
    view.request = SimpleNamespace(query_params={})
    with mock.patch.object(views, "filter_by_activity", return_value="QS") as fa:
        assert view.get_queryset() == "QS"
    assert fa.call_args.args[1] == ActivityType.WALKING


def test_get_queryset_user_branch_and_wheeling():
    view = views.GoalsView()
    view.request = SimpleNamespace(query_params={"user": "device-1", "activity_type": "wheeling"})
    with mock.patch.object(views, "filter_by_activity", return_value="QS") as fa:
        view.get_queryset()
    assert fa.call_args.args[1] == ActivityType.WHEELING


def test_str_with_and_without_user():
    assert str(Goal(text="Be active", user="device-1")) == "Be active-device-1"
    assert str(Goal(text="Be active")) == "Be active"
