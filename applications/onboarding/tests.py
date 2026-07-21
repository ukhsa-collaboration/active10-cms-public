"""DB-free tests (pytest + mock). No django_db marker => DB access is blocked."""

from types import SimpleNamespace
from unittest import mock

import applications.onboarding.serializers as serializers
import applications.onboarding.views as views
from utils.activity import ActivityType


class TestOnboardingView:
    def test_get_object_picks_by_activity(self):
        view = views.OnboardingView()
        view.request = SimpleNamespace(query_params={"activity_type": "wheeling"})
        with mock.patch.object(views, "pick_by_activity", return_value="OBJ") as pick:
            assert view.get_object() == "OBJ"
        assert pick.call_args.args[1] == ActivityType.WHEELING

    def test_get_serializer_context_carries_activity(self):
        view = views.OnboardingView()
        view.request = SimpleNamespace(query_params={})
        view.format_kwarg = None
        context = view.get_serializer_context()
        assert context["activity"] == ActivityType.WALKING


class TestOnboardingSerializer:
    def test_ready_to_get_started_uses_activity_from_context(self):
        serializer = serializers.OnboardingSerializer(context={"activity": ActivityType.WHEELING})
        with (
            mock.patch.object(serializers, "pick_by_activity", return_value="READY") as pick,
            mock.patch.object(serializers, "ReadyToGetStartedSerializer", return_value=SimpleNamespace(data={"k": 1})),
        ):
            assert serializer.get_ready_to_get_started(SimpleNamespace()) == {"k": 1}
        assert pick.call_args.args[1] == ActivityType.WHEELING

    def test_ready_to_get_started_defaults_to_walking(self):
        serializer = serializers.OnboardingSerializer()
        with (
            mock.patch.object(serializers, "pick_by_activity", return_value="READY") as pick,
            mock.patch.object(serializers, "ReadyToGetStartedSerializer", return_value=SimpleNamespace(data={})),
        ):
            serializer.get_ready_to_get_started(SimpleNamespace())
        assert pick.call_args.args[1] == ActivityType.WALKING
