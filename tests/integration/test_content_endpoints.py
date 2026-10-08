import pytest

from .utils import assert_fields, assert_status, get_json, is_url

DEFAULT_PARAMS = {"format": "json"}


def _get_json(client, base_url, path, params=None):
    return get_json(client, f"{base_url}{path}", params)


def _looks_like_url(value):
    if not isinstance(value, str):
        return False
    return is_url(value) or value.startswith("/")


def _assert_links_resolve(client, urls, *, description: str) -> None:
    assert urls, f"No URLs collected for {description}"
    failures = []
    for url in urls:
        try:
            resp = client.get(url, follow_redirects=True)
            if resp.status_code >= 400:
                failures.append(f"{url} -> {resp.status_code}")
        except Exception as exc:  # pragma: no cover - defensive
            failures.append(f"{url} -> EXC: {exc!r}")
    assert not failures, f"{description} link failures:\n" + "\n".join(failures)


def test_about_one_you_shape(client, base_url, require_content):
    data = _get_json(client, base_url, "/api/v1/active10/about-one-you/")
    assert isinstance(data, dict)
    require_content(data, "About One You")
    assert isinstance(data.get("about"), dict)
    assert isinstance(data["about"].get("text"), str)

    apps = data.get("apps")
    assert isinstance(apps, list)
    require_content(apps, "About One You apps")

    for app in apps:
        assert_fields(app, {"id": int, "name": str, "description": str})
        for key in ("ios", "android", "icon"):
            value = app.get(key)
            assert value is None or (isinstance(value, str) and is_url(value)), f"Invalid {key}: {value!r}"


@pytest.mark.external
def test_about_one_you_links_resolve(client, base_url, require_content):
    data = _get_json(client, base_url, "/api/v1/active10/about-one-you/")
    urls = []
    for app in data.get("apps", []):
        for key in ("ios", "android", "icon"):
            value = app.get(key)
            if isinstance(value, str) and is_url(value):
                urls.append(value)
    require_content(urls, "About One You app links")
    _assert_links_resolve(client, urls, description="About One You apps")


def test_faq_list_shape(client, base_url, require_content):
    faqs = _get_json(client, base_url, "/api/v1/active10/faq/")
    assert isinstance(faqs, list)
    require_content(faqs, "FAQs")
    for question in faqs:
        assert_fields(question, {"id": int, "title": str, "text": str})


def test_discover_shape(client, base_url, require_content):
    data = _get_json(client, base_url, "/api/v1/active10/discover/")
    assert isinstance(data, dict)

    discover_items = data.get("discover")
    assert isinstance(discover_items, list)
    require_content(discover_items, "Discover items")

    for item in discover_items:
        assert_fields(
            item,
            {
                "id": int,
                "published": bool,
                "description": str,
                "action": str,
                "colour": str,
                "border_colour": str,
                "list_order": int,
            },
        )
        for key in ("header_image", "name_image_url"):
            if item.get(key):
                assert _looks_like_url(item[key])
        splash = item.get("splash_screen")
        if splash is not None:
            assert_fields(splash, {"title": str})
            for key in ("link", "android_link", "ios_link"):
                if splash.get(key):
                    assert is_url(splash[key])

    tips = data.get("tips")
    require_content(tips, "Tips")
    for tip in tips:
        assert_fields(tip, {"id": int, "title": str, "message": str})
        if tip.get("image"):
            assert _looks_like_url(tip["image"])


def test_articles_list_and_detail(client, base_url, require_content):
    articles = _get_json(client, base_url, "/api/v1/active10/articles/")
    assert isinstance(articles, list)

    require_content(articles, "Articles")

    for item in articles:
        assert_fields(item, {"id": int, "slug": str, "title": str, "description": str, "destination": dict})
    article = articles[0]
    for key in ("id", "slug", "title", "description", "destination", "categoryId"):
        assert key in article, f"Missing '{key}' in article payload"

    assert isinstance(article["destination"], dict)
    for platform in ("ios", "android"):
        assert platform in article["destination"], "Destination missing platform value"

    if article.get("imageUrl"):
        assert is_url(article["imageUrl"])

    detail = _get_json(client, base_url, f"/api/v1/active10/articles/{article['id']}/")
    assert detail["id"] == article["id"]
    assert detail["slug"] == article["slug"]


def test_article_categories_list_and_detail(client, base_url, require_content):
    categories = _get_json(client, base_url, "/api/v1/active10/categories/")
    assert isinstance(categories, list)

    require_content(categories, "Categories")

    for item in categories:
        assert_fields(item, {"id": int, "name": str})
    category = categories[0]
    for key in ("id", "name"):
        assert key in category

    detail = _get_json(client, base_url, f"/api/v1/active10/categories/{category['id']}/")
    assert detail["id"] == category["id"]


def test_dynamic_texts_shape(client, base_url):
    data = _get_json(client, base_url, "/api/v1/active10/dynamic-texts/")
    assert isinstance(data, dict)
    assert "my_walks_dynamic_text" in data
    assert "todays_walks_dynamic_text" in data
    assert isinstance(data["my_walks_dynamic_text"], dict)
    assert isinstance(data["todays_walks_dynamic_text"], dict)

    for target, entries in data["todays_walks_dynamic_text"].items():
        assert isinstance(entries, dict), f"Expected dict for {target}"


def test_global_rules_shape(client, base_url, require_content):
    data = _get_json(client, base_url, "/api/v1/active10/global_rules/")
    assert isinstance(data, dict)

    for key in ("terms_conditions", "app"):
        assert key in data

    assert_fields(data["terms_conditions"], {"text": str})
    assert isinstance(data["app"], dict)
    require_content(data["app"], "App version data")


def test_goals_list_shape(client, base_url, require_content):
    goals = _get_json(client, base_url, "/api/v1/active10/goals/")
    require_content(goals, "Goals")
    for goal in goals:
        assert_fields(goal, {"id": int, "text": str})


def test_goals_post_requires_valid_payload(client, base_url):
    response = client.post(
        f"{base_url}/api/v1/active10/goals/",
        json={},
        params=DEFAULT_PARAMS,
    )
    assert_status(response, 400)
    body = response.json()
    assert "text" in body, "Validation error should include 'text'"


def test_how_it_works_list_shape(client, base_url, require_content):
    steps = _get_json(client, base_url, "/api/v1/active10/how-it-works/")
    require_content(steps, "How it works")
    for step in steps:
        assert_fields(step, {"title": str, "description": str})


def test_legals_list_shape(client, base_url, require_content):
    legals = _get_json(client, base_url, "/api/v1/active10/legals/")
    assert isinstance(legals, list)

    require_content(legals, "Legals")

    for legal in legals:
        assert_fields(legal, {"title": str, "shouldAccept": bool, "version": int})
        assert "pageType" in legal
        assert legal["pageType"] is None or isinstance(legal["pageType"], str)
        assert isinstance(legal.get("content"), (dict, list))
    # LegalSerializer intentionally omits IDs; there is no exposed detail lookup.


def test_notifications_shape(client, base_url):
    data = _get_json(client, base_url, "/api/v1/active10/notifications/")
    assert isinstance(data, dict)
    for key in ("onboarding", "lapsed", "reminder"):
        assert key in data

    assert isinstance(data["onboarding"], list)
    assert isinstance(data["lapsed"], list)

    if data.get("local") is not None:
        assert isinstance(data["local"], list)


def test_onboarding_shape(client, base_url):
    data = _get_json(client, base_url, "/api/v1/active10/onboarding/")
    assert isinstance(data, dict)
    for key in ("ready_to_get_started", "motion_fitness", "location", "notifications", "goals"):
        assert key in data


def test_tips_list_shape(client, base_url, require_content):
    tips = _get_json(client, base_url, "/api/v1/active10/tips/")
    require_content(tips, "Tips")
    for tip in tips:
        assert_fields(tip, {"id": int, "title": str, "description": str})
        if tip.get("image"):
            assert _looks_like_url(tip["image"])


def test_views_list_and_detail(client, base_url, require_content):
    list_path = "/api/v1/active10/views"
    views = _get_json(client, base_url, list_path)
    assert isinstance(views, list)

    require_content(views, "Views")

    for item in views:
        assert_fields(item, {"id": int, "slug": str, "title": str})
    view = views[0]
    for key in ("id", "slug", "title"):
        assert key in view

    detail = _get_json(client, base_url, f"/api/v1/active10/views{view['id']}/")
    assert detail["id"] == view["id"]


def test_walking_plans_list_and_detail(client, base_url, require_content):
    plans = _get_json(client, base_url, "/api/v1/active10/walking-plans/plans/")
    assert isinstance(plans, list)

    require_content(plans, "Walking plans")

    for item in plans:
        assert_fields(item, {"id": int, "plan_name": str, "plan_duration_weeks": int})
    plan = plans[0]
    for key in ("id", "plan_name", "plan_duration_weeks"):
        assert key in plan

    if plan.get("image"):
        assert _looks_like_url(plan["image"])

    detail = _get_json(client, base_url, f"/api/v1/active10/walking-plans/plans/{plan['id']}/")
    assert detail["id"] == plan["id"]


@pytest.mark.external
def test_discover_image_links_resolve(client, base_url, require_content):
    data = _get_json(client, base_url, "/api/v1/active10/discover/")
    urls = [tip["image"] for tip in data.get("tips", []) if tip.get("image")]
    require_content(urls, "Discover tip images")
    _assert_links_resolve(client, urls, description="Discover tip images")


@pytest.mark.parametrize(
    "path",
    (
        "/api/v1/active10/articles/",
        "/api/v1/active10/categories/",
        "/api/v1/active10/dynamic-texts/",
        "/api/v1/active10/global_rules/",
        "/api/v1/active10/legals/",
        "/api/v1/active10/notifications/",
        "/api/v1/active10/onboarding/",
        "/api/v1/active10/tips/",
        "/api/v1/active10/views",
        "/api/v1/active10/walking-plans/plans/",
    ),
)
def test_post_not_allowed_for_read_only_endpoints(client, base_url, path):
    response = client.post(f"{base_url}{path}", json={"test": True}, params=DEFAULT_PARAMS)
    assert_status(response, 405)
