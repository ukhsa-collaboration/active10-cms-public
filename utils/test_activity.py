"""Unit tests for the activity-type tagging helpers.

These are pure-logic tests: no database, no HTTP. They exercise the branching
in ``utils.activity`` (param resolution, the ``both`` cascade, the single-record
fallback) using fakes, so the suite stays fast and DB-free.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from utils.activity import (
    ActivityType,
    ActivityTypeModel,
    filter_by_activity,
    pick_by_activity,
    resolve_activity,
)


def _request(params):
    """A stand-in for a DRF request — only ``query_params`` is used."""
    return SimpleNamespace(query_params=params)


class TestResolveActivity:
    def test_missing_param_defaults_to_walking(self):
        assert resolve_activity(_request({})) == ActivityType.WALKING

    def test_walking_param(self):
        assert resolve_activity(_request({"activity_type": "walking"})) == ActivityType.WALKING

    def test_wheeling_param(self):
        assert resolve_activity(_request({"activity_type": "wheeling"})) == ActivityType.WHEELING

    def test_invalid_param_falls_back_to_walking(self):
        assert resolve_activity(_request({"activity_type": "nonsense"})) == ActivityType.WALKING

    def test_both_param_is_requestable(self):
        # 'both' asks for the full catalogue (walking + wheeling + both).
        assert resolve_activity(_request({"activity_type": "both"})) == ActivityType.BOTH


class TestFilterByActivity:
    def test_filters_on_requested_value_plus_both(self):
        queryset = MagicMock(name="queryset")
        result = filter_by_activity(queryset, ActivityType.WHEELING)

        queryset.filter.assert_called_once_with(activity_type__in=[ActivityType.WHEELING, ActivityType.BOTH])
        assert result is queryset.filter.return_value

    def test_walking_cascade(self):
        queryset = MagicMock(name="queryset")
        filter_by_activity(queryset, ActivityType.WALKING)
        queryset.filter.assert_called_once_with(activity_type__in=[ActivityType.WALKING, ActivityType.BOTH])

    def test_both_returns_full_queryset_unfiltered(self):
        queryset = MagicMock(name="queryset")
        result = filter_by_activity(queryset, ActivityType.BOTH)

        queryset.filter.assert_not_called()
        assert result is queryset


def _rows(*activity_types):
    """Rows tagged with an activity type, ``pk`` ascending in argument order."""
    return [SimpleNamespace(pk=pk, activity_type=value) for pk, value in enumerate(activity_types, start=1)]


class _FakeQuerySet:
    """Minimal queryset double over rows carrying ``pk`` and ``activity_type``."""

    def __init__(self, rows):
        self._rows = list(rows)

    def filter(self, **kwargs):
        return _FakeQuerySet([row for row in self._rows if row.activity_type == kwargs["activity_type"]])

    def order_by(self, field):
        assert field == "-pk", f"unexpected ordering: {field}"
        return _FakeQuerySet(sorted(self._rows, key=lambda row: row.pk, reverse=True))

    def first(self):
        return self._rows[0] if self._rows else None


class TestPickByActivity:
    def test_exact_match_wins(self):
        rows = _rows("walking", "wheeling", "both")
        assert pick_by_activity(_FakeQuerySet(rows), ActivityType.WHEELING) is rows[1]

    def test_newest_exact_match_wins(self):
        # Several wheeling records authored → serve the most recent one.
        rows = _rows("wheeling", "both", "wheeling")
        assert pick_by_activity(_FakeQuerySet(rows), ActivityType.WHEELING) is rows[2]

    def test_falls_back_to_both_when_no_exact_match(self):
        rows = _rows("walking", "both")
        assert pick_by_activity(_FakeQuerySet(rows), ActivityType.WHEELING) is rows[1]

    def test_falls_back_to_newest_both(self):
        rows = _rows("both", "both")
        assert pick_by_activity(_FakeQuerySet(rows), ActivityType.WHEELING) is rows[1]

    def test_returns_none_when_only_another_journey_authored(self):
        # No wheeling and no 'both' copy → serve nothing rather than walking copy.
        assert pick_by_activity(_FakeQuerySet(_rows("walking")), ActivityType.WHEELING) is None

    def test_returns_none_when_empty(self):
        assert pick_by_activity(_FakeQuerySet([]), ActivityType.WHEELING) is None

    def test_returns_none_for_unknown_tag(self):
        assert pick_by_activity(_FakeQuerySet(_rows("wheeling")), "nonsense") is None


class TestActivityTypeModel:
    def test_default_is_walking(self):
        field = ActivityTypeModel._meta.get_field("activity_type")
        assert field.default == ActivityType.WALKING

    def test_choices_are_walking_wheeling_both(self):
        field = ActivityTypeModel._meta.get_field("activity_type")
        assert {value for value, _label in field.choices} == {"walking", "wheeling", "both"}
