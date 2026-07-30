"""DB-free tests (pytest + mock). No django_db marker => DB access is blocked."""

from types import SimpleNamespace
from unittest import mock

import applications.notifications.serializers as serializers
import applications.notifications.views as views


class TestNotificationsView:
    def test_get_returns_serializer_data(self):
        view = views.NotificationsView()
        request = SimpleNamespace(query_params={})
        fake_serializer = mock.MagicMock()
        fake_serializer.is_valid.return_value = True
        fake_serializer.data = {"onboarding": [], "local": []}
        view.serializer_class = mock.MagicMock(return_value=fake_serializer)
        response = view.get(request)
        assert response.data == {"onboarding": [], "local": []}
        # the request is threaded into the serializer context for activity resolution
        assert view.serializer_class.call_args.kwargs["context"]["request"] is request


class TestNotificationsSerializer:
    def _serializer(self, params):
        return serializers.NotificationsSerializer(context={"request": SimpleNamespace(query_params=params)})

    def test_to_representation_empty(self):
        serializer = self._serializer({})
        with (
            mock.patch.object(serializers, "filter_by_activity", return_value=[]),
            mock.patch.object(serializers.LocalNotification, "objects") as local,
        ):
            local.all.return_value = []
            data = serializer.to_representation(None)
        assert data == {"onboarding": [], "lapsed": [], "reminders": [], "reminder": "", "local": []}

    def test_to_representation_with_data(self):
        serializer = self._serializer({"activity_type": "wheeling"})
        with (
            mock.patch.object(serializers, "filter_by_activity", return_value=[]),
            mock.patch.object(serializers, "OnboardingSerializer", return_value=SimpleNamespace(data=[{"copy": "o"}])),
            mock.patch.object(serializers, "LapsedSerializer", return_value=SimpleNamespace(data=[{"copy": "l"}])),
            mock.patch.object(
                serializers,
                "ReminderSerializer",
                return_value=SimpleNamespace(data=[{"copy": "r", "activity_type": "walking"}]),
            ),
            mock.patch.object(
                serializers, "LocalNotificationSerializer", return_value=SimpleNamespace(data=[{"slug": "s"}])
            ),
        ):
            data = serializer.to_representation(None)
        assert data["reminder"] == "r"
        assert data["reminders"] == [{"copy": "r", "activity_type": "walking"}]
        assert data["onboarding"] == [{"copy": "o"}]
        assert data["local"] == [{"slug": "s"}]

    def test_reminder_scalar_holds_the_walking_copy(self):
        # `reminders` carries every journey's copy; the legacy scalar `reminder` stays
        # walking-only, so the v1 app keeps getting the copy it always got.
        serializer = self._serializer({"activity_type": "both"})
        rows = [{"copy": "wheel", "activity_type": "wheeling"}, {"copy": "walk", "activity_type": "walking"}]
        with (
            mock.patch.object(serializers, "filter_by_activity", return_value=[]),
            mock.patch.object(serializers, "ReminderSerializer", return_value=SimpleNamespace(data=rows)),
            mock.patch.object(serializers.LocalNotification, "objects") as local,
        ):
            local.all.return_value = []
            data = serializer.to_representation(None)

        assert data["reminder"] == "walk"
        assert data["reminders"] == rows

    def test_reminder_scalar_empty_when_no_walking_copy(self):
        serializer = self._serializer({"activity_type": "wheeling"})
        rows = [{"copy": "wheel", "activity_type": "wheeling"}]
        with (
            mock.patch.object(serializers, "filter_by_activity", return_value=[]),
            mock.patch.object(serializers, "ReminderSerializer", return_value=SimpleNamespace(data=rows)),
            mock.patch.object(serializers.LocalNotification, "objects") as local,
        ):
            local.all.return_value = []
            data = serializer.to_representation(None)

        assert data["reminder"] == ""
        assert data["reminders"] == rows

    def test_to_representation_without_request_defaults_walking(self):
        serializer = serializers.NotificationsSerializer()
        with (
            mock.patch.object(serializers, "filter_by_activity", return_value=[]) as fa,
            mock.patch.object(serializers.LocalNotification, "objects") as local,
        ):
            local.all.return_value = []
            serializer.to_representation(None)
        assert fa.call_args.args[1] == "walking"

    def test_onboarding_get_userinfo_flattens(self):
        serializer = serializers.OnboardingSerializer()
        obj = SimpleNamespace(
            userinfo=SimpleNamespace(
                all=lambda: [SimpleNamespace(label="name", value="A"), SimpleNamespace(label="age", value="30")]
            )
        )
        assert serializer.get_userinfo(obj) == {"name": "A", "age": "30"}

    def test_lapsed_get_userinfo_flattens(self):
        serializer = serializers.LapsedSerializer()
        obj = SimpleNamespace(userinfo=SimpleNamespace(all=lambda: [SimpleNamespace(label="name", value="A")]))
        assert serializer.get_userinfo(obj) == {"name": "A"}
