"""Unit tests for the admin clone helper.

Pure-logic tests: no database, no HTTP. ``CloneAdminMixin`` is exercised with
fakes for the model/manager and monkeypatched module globals (``reverse``,
``redirect``, ``messages``, ``transaction``, ``get_object_or_404``), so the suite
stays fast and DB-free. The two per-model overrides (Discover's OneToOne splash
screen, Article's M2M through-rows) are tested by calling the bound methods with
fakes — they don't use ``self``, so no admin construction or DB is needed.
"""

from contextlib import nullcontext
from types import SimpleNamespace

import pytest

from utils.admin import CloneAdminMixin


class _FakeRow:
    """A model-instance double. Only the attributes passed in exist, so
    ``hasattr(row, "published")`` reflects whether the model has that field."""

    def __init__(self, events=None, full_clean_error=None, **attrs):
        self.__dict__.update(attrs)
        self._events = events
        self._full_clean_error = full_clean_error
        self.saved = False
        self.full_cleaned = False

    def full_clean(self, *args, **kwargs):
        self.full_cleaned = True
        if self._full_clean_error is not None:
            raise self._full_clean_error

    def save(self):
        self.saved = True
        if self._events is not None:
            self._events.append("save")


class _FakeManager:
    def __init__(self, row):
        self._row = row

    def get(self, pk):
        self.requested_pk = pk
        return self._row


class _FakeModel:
    """Stands in for the model class: ``.objects.get`` and ``._meta``."""

    def __init__(self, row, app_label="faq", model_name="faq"):
        self.objects = _FakeManager(row)
        self._meta = SimpleNamespace(app_label=app_label, model_name=model_name)


class _Base:
    """The slice of ``admin.ModelAdmin`` the mixin calls via ``super()``/``self``."""

    def __init__(self, model, list_display=(), can_add=True):
        self.model = model
        self._list_display = list(list_display)
        self._can_add = can_add

    def get_list_display(self, request):
        return list(self._list_display)

    def has_add_permission(self, request):
        return self._can_add


class _Admin(CloneAdminMixin, _Base):
    pass


class TestGetListDisplay:
    def test_appends_clone_button(self):
        admin = _Admin(_FakeModel(_FakeRow()), list_display=["title", "activity_type"])
        assert admin.get_list_display(request=None) == ["title", "activity_type", "clone_button"]

    def test_does_not_duplicate_clone_button(self):
        admin = _Admin(_FakeModel(_FakeRow()), list_display=["title", "clone_button"])
        assert admin.get_list_display(request=None).count("clone_button") == 1

    def test_leaves_original_columns_untouched(self):
        admin = _Admin(_FakeModel(_FakeRow()), list_display=["a", "b"])
        admin.get_list_display(request=None)
        # The admin's declared list_display is not mutated in place.
        assert admin._list_display == ["a", "b"]


class TestCloneButton:
    def test_renders_anchor_to_clone_url(self, monkeypatch):
        monkeypatch.setattr("utils.admin.reverse", lambda name, args: f"/admin/clone/{args[0]}/")
        admin = _Admin(_FakeModel(_FakeRow()))
        html = admin.clone_button(SimpleNamespace(pk=7))
        assert str(html) == '<a class="button" href="/admin/clone/7/">Clone</a>'

    def test_reverses_the_per_model_clone_route(self, monkeypatch):
        captured = {}

        def fake_reverse(name, args):
            captured["name"] = name
            captured["args"] = args
            return "/x/"

        monkeypatch.setattr("utils.admin.reverse", fake_reverse)
        admin = _Admin(_FakeModel(_FakeRow(), app_label="discover", model_name="discover"))
        admin.clone_button(SimpleNamespace(pk=3))
        assert captured["name"] == "admin:discover_discover_clone"
        assert captured["args"] == [3]


class TestCloneObject:
    def test_resets_pk_and_id(self):
        row = _FakeRow(pk=5, id=5, title="Hello")
        admin = _Admin(_FakeModel(row), list_display=[])
        admin.clone_name_field = "title"
        admin.clone_object(SimpleNamespace(pk=5))
        assert row.pk is None and row.id is None

    def test_appends_clone_to_name_field(self):
        row = _FakeRow(pk=5, id=5, title="Walk 10 min")
        admin = _Admin(_FakeModel(row))
        admin.clone_name_field = "title"
        admin.clone_object(SimpleNamespace(pk=5))
        assert row.title == "Walk 10 min clone"

    def test_no_rename_when_field_not_configured(self):
        row = _FakeRow(pk=1, id=1, title="Untouched")
        admin = _Admin(_FakeModel(row))
        admin.clone_name_field = None
        admin.clone_object(SimpleNamespace(pk=1))
        assert row.title == "Untouched"

    def test_no_rename_when_value_is_empty(self):
        # name_text on Discover is nullable; don't produce a stray " clone".
        row = _FakeRow(pk=1, id=1, name_text="")
        admin = _Admin(_FakeModel(row))
        admin.clone_name_field = "name_text"
        admin.clone_object(SimpleNamespace(pk=1))
        assert row.name_text == ""

    def test_unpublishes_when_model_has_published(self):
        row = _FakeRow(pk=1, id=1, title="t", published=True)
        admin = _Admin(_FakeModel(row))
        admin.clone_name_field = "title"
        admin.clone_object(SimpleNamespace(pk=1))
        assert row.published is False

    def test_leaves_models_without_published_alone(self):
        row = _FakeRow(pk=1, id=1, title="t")
        admin = _Admin(_FakeModel(row))
        admin.clone_name_field = "title"
        admin.clone_object(SimpleNamespace(pk=1))
        assert not hasattr(row, "published")

    def test_rename_false_keeps_original_name(self):
        row = _FakeRow(pk=1, id=1, title="Walk 10 min")
        admin = _Admin(_FakeModel(row))
        admin.clone_name_field = "title"
        admin.clone_object(SimpleNamespace(pk=1), rename=False)
        assert row.title == "Walk 10 min"

    def test_validates_before_saving(self):
        row = _FakeRow(pk=1, id=1, title="t")
        admin = _Admin(_FakeModel(row))
        admin.clone_object(SimpleNamespace(pk=1))
        assert row.full_cleaned is True

    def test_saves_the_clone(self):
        row = _FakeRow(pk=1, id=1, title="t")
        admin = _Admin(_FakeModel(row))
        admin.clone_object(SimpleNamespace(pk=1))
        assert row.saved is True

    def test_returns_the_clone(self):
        row = _FakeRow(pk=1, id=1, title="t")
        admin = _Admin(_FakeModel(row))
        assert admin.clone_object(SimpleNamespace(pk=1)) is row

    def test_hooks_run_before_and_after_save(self):
        events = []
        row = _FakeRow(events=events, pk=1, id=1, title="t")

        class _Recording(_Admin):
            def before_save_clone(self, original, clone):
                events.append("before")

            def after_save_clone(self, original, clone):
                events.append("after")

        admin = _Recording(_FakeModel(row))
        admin.clone_object(SimpleNamespace(pk=1))
        assert events == ["before", "save", "after"]


class TestCloneView:
    def _patch_helpers(self, monkeypatch, atomic_used):
        monkeypatch.setattr("utils.admin.reverse", lambda name, **kw: "/changelist/")
        monkeypatch.setattr("utils.admin.redirect", lambda url: ("redirect", url))
        monkeypatch.setattr("utils.admin.messages", SimpleNamespace(
            success=lambda req, msg: atomic_used.setdefault("messages", []).append(("success", msg)),
            error=lambda req, msg: atomic_used.setdefault("messages", []).append(("error", msg)),
        ))

    def test_denies_when_no_add_permission(self, monkeypatch):
        log = {}
        self._patch_helpers(monkeypatch, log)
        cloned = []

        class _Admin2(_Admin):
            def clone_object(self, original):
                cloned.append(original)

        admin = _Admin2(_FakeModel(_FakeRow()), can_add=False)
        result = admin.clone_view(request=object(), object_id=1)

        assert result == ("redirect", "/changelist/")
        assert cloned == []  # nothing cloned
        assert log["messages"] == [("error", "You do not have permission to clone this object.")]

    def test_clones_within_a_transaction_and_redirects(self, monkeypatch):
        log = {}
        self._patch_helpers(monkeypatch, log)
        original = SimpleNamespace(pk=9)
        monkeypatch.setattr("utils.admin.get_object_or_404", lambda model, pk: original)

        atomic_calls = []

        def fake_atomic():
            atomic_calls.append(True)
            return nullcontext()

        monkeypatch.setattr("utils.admin.transaction", SimpleNamespace(atomic=fake_atomic))

        cloned = []

        class _Admin2(_Admin):
            def clone_object(self, obj):
                cloned.append(obj)
                return SimpleNamespace(pk=10, __str__=lambda self: "Clone")

        admin = _Admin2(_FakeModel(_FakeRow()), can_add=True)
        result = admin.clone_view(request=object(), object_id=9)

        assert cloned == [original]
        assert atomic_calls == [True]  # wrapped in a transaction
        assert result == ("redirect", "/changelist/")
        assert log["messages"][0][0] == "success"

    def test_save_error_routes_to_the_error_response(self, monkeypatch):
        log = {}
        self._patch_helpers(monkeypatch, log)
        original = SimpleNamespace(pk=9)
        monkeypatch.setattr("utils.admin.get_object_or_404", lambda model, pk: original)
        monkeypatch.setattr("utils.admin.transaction", SimpleNamespace(atomic=lambda: nullcontext()))

        from django.db import DataError

        class _Admin2(_Admin):
            def clone_object(self, obj, rename=True):
                raise DataError("value too long for type character varying(20)")

            def clone_error_response(self, request, original, exc):
                return ("error-form", exc)

        admin = _Admin2(_FakeModel(_FakeRow()), can_add=True)
        result = admin.clone_view(request=object(), object_id=9)

        # No success message; control handed to the graceful error response.
        assert "messages" not in log
        assert result[0] == "error-form"


class TestDiscoverCloneRelations:
    """DiscoverAdmin.before_save_clone duplicates the OneToOne SplashScreen."""

    def _method(self):
        from applications.discover.admin import DiscoverAdmin

        # before_save_clone doesn't use self — skip __init__ (no admin_site needed).
        return object.__new__(DiscoverAdmin).before_save_clone

    def test_duplicates_the_splash_screen(self):
        splash = _FakeRow(pk=10, id=10)
        original = SimpleNamespace(splash_screen_id=10, splash_screen=splash)
        clone = _FakeRow()

        self._method()(original, clone)

        assert splash.pk is None and splash.id is None
        assert splash.saved is True
        assert clone.splash_screen is splash

    def test_no_op_without_a_splash_screen(self):
        original = SimpleNamespace(splash_screen_id=None, splash_screen=None)
        clone = _FakeRow()

        self._method()(original, clone)

        assert not hasattr(clone, "splash_screen")


class _FakeRelManager:
    def __init__(self, rows):
        self._rows = list(rows)
        self.created = []
        self.filtered_with = None

    def filter(self, **kwargs):
        self.filtered_with = kwargs
        return list(self._rows)

    def create(self, **kwargs):
        self.created.append(kwargs)
        return SimpleNamespace(**kwargs)


class _FakeRelModel:
    def __init__(self, rows=()):
        self.objects = _FakeRelManager(rows)


class TestArticleCloneRelations:
    """ArticleAdmin.after_save_clone re-creates through-rows on the same targets."""

    def test_recreates_views_related_and_content_views(self, monkeypatch):
        from applications.articles import admin as article_admin

        views = _FakeRelModel([SimpleNamespace(view="V1", order=1)])
        related = _FakeRelModel([SimpleNamespace(related_article="A2", order=2)])
        content = _FakeRelModel([SimpleNamespace(view="V3", order=3)])
        monkeypatch.setattr(article_admin, "ArticleView", views)
        monkeypatch.setattr(article_admin, "ArticleRelated", related)
        monkeypatch.setattr(article_admin, "ContentView", content)

        original = SimpleNamespace(pk=1)
        clone = SimpleNamespace(pk=2)
        method = object.__new__(article_admin.ArticleAdmin).after_save_clone
        method(original, clone)

        # Each relation was read off the original...
        assert views.objects.filtered_with == {"article": original}
        # ...and re-created pointing at the clone with the same shared targets.
        assert views.objects.created == [{"article": clone, "view": "V1", "order": 1}]
        assert related.objects.created == [{"article": clone, "related_article": "A2", "order": 2}]
        assert content.objects.created == [{"article": clone, "view": "V3", "order": 3}]

    def test_clone_with_no_relations_creates_nothing(self, monkeypatch):
        from applications.articles import admin as article_admin

        empty = lambda: _FakeRelModel([])
        views, related, content = empty(), empty(), empty()
        monkeypatch.setattr(article_admin, "ArticleView", views)
        monkeypatch.setattr(article_admin, "ArticleRelated", related)
        monkeypatch.setattr(article_admin, "ContentView", content)

        method = object.__new__(article_admin.ArticleAdmin).after_save_clone
        method(SimpleNamespace(pk=1), SimpleNamespace(pk=2))

        assert views.objects.created == []
        assert related.objects.created == []
        assert content.objects.created == []
