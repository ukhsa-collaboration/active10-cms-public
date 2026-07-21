"""DB-free tests for the articles activity-type wiring.

No `django_db` marker is used anywhere here, so pytest-django blocks real
database access — any accidental query fails the test loudly. Querysets are
mocked and serializer inputs are plain `SimpleNamespace` stand-ins.
"""

from types import SimpleNamespace
from unittest import mock

import applications.articles.views as views
from applications.articles.serializers import ArticleSerializer
from utils.activity import ActivityType


def _view(params):
    view = views.ArticlesViewSet()
    view.request = SimpleNamespace(query_params=params)
    view.format_kwarg = None
    return view


class TestArticlesViewList:
    def test_invalid_user_group_returns_400(self):
        view = _view({"user_group": "bogus"})
        with mock.patch.object(view, "get_queryset", return_value=mock.MagicMock()):
            response = view.list(view.request)
        assert response.status_code == 400

    def test_default_applies_users_and_walking(self):
        view = _view({})
        qs = mock.MagicMock()
        with (
            mock.patch.object(view, "get_queryset", return_value=qs),
            mock.patch.object(views, "filter_by_activity", return_value=qs) as fa,
            mock.patch.object(view, "get_serializer", return_value=SimpleNamespace(data=["ok"])),
        ):
            response = view.list(view.request)
        assert response.data == ["ok"]
        # default user_group == "users" -> cascade with all_users
        qs.filter.assert_called_once_with(user_group__in=["users", "all_users"])
        assert fa.call_args.args[1] == ActivityType.WALKING

    def test_all_users_branch_and_wheeling(self):
        view = _view({"user_group": "all_users", "activity_type": "wheeling"})
        qs = mock.MagicMock()
        with (
            mock.patch.object(view, "get_queryset", return_value=qs),
            mock.patch.object(views, "filter_by_activity", return_value=qs) as fa,
            mock.patch.object(view, "get_serializer", return_value=SimpleNamespace(data=[])),
        ):
            view.list(view.request)
        qs.filter.assert_called_once_with(user_group="all_users")
        assert fa.call_args.args[1] == ActivityType.WHEELING


class TestArticleSerializerMethods:
    """Cover the SerializerMethodField bodies without touching the DB."""

    def setup_method(self):
        self.s = ArticleSerializer()

    def test_destination(self):
        obj = SimpleNamespace(destination_ios="i", destination_android="a")
        assert self.s.get_destination(obj) == {"ios": "i", "android": "a"}

    def test_view_and_content_view_ids(self):
        obj = SimpleNamespace(
            articleview_set=SimpleNamespace(all=lambda: [SimpleNamespace(view_id=1), SimpleNamespace(view_id=2)]),
            contentview_set=SimpleNamespace(all=lambda: [SimpleNamespace(view_id=9)]),
        )
        assert self.s.get_view_ids(obj) == [1, 2]
        assert self.s.get_content_view_ids(obj) == [9]

    def test_related_article_ids(self):
        obj = SimpleNamespace(parent_article=SimpleNamespace(all=lambda: [SimpleNamespace(related_article_id=7)]))
        assert self.s.get_related_article_ids(obj) == [7]

    def test_category_name_and_position(self):
        obj = SimpleNamespace(category=SimpleNamespace(name="cat", position=3))
        assert self.s.get_category_name(obj) == "cat"
        assert self.s.get_category_position(obj) == 3

    def test_image_url_empty(self):
        assert self.s.get_image_url(SimpleNamespace(image=None)) == ""

    def test_content_as_json_runs(self):
        # Just exercise the path; html_text_to_json handles empty content.
        assert self.s.get_content_as_json(SimpleNamespace(content="")) is not None
