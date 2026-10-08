"""Read-only rewards contracts, tested independently for each API version."""

from urllib.parse import quote
from uuid import uuid4

import pytest

from .utils import assert_fields, assert_status, get_json, is_url

pytestmark = pytest.mark.parametrize("version", ["v1", "v2", "v3"])


def _path(version, slug=None):
    # The registered router prefix ends in '/', so detail routes contain '//'.
    path = f"/api/{version}/active10/rewards/"
    return path if slug is None else f"{path}/{quote(slug, safe='')}"


def test_rewards_list_contract(client, version):
    rewards = get_json(client, _path(version))
    assert isinstance(rewards, list)
    for reward in rewards:
        assert_fields(
            reward,
            {
                "id": int,
                "title": str,
                "category": str,
                "slug": str,
                "text": str,
                "how_to": str,
                "position": int,
                "created_at": str,
                "updated_at": str,
            },
        )
        assert reward["id"] > 0
        assert reward["slug"]
        assert reward["share"] is None or isinstance(reward["share"], str)
        for field in ("on_image", "off_image", "animation"):
            assert field in reward
            assert reward[field] is None or is_url(reward[field]), f"Invalid {field}: {reward[field]!r}"
        if version == "v1":
            assert reward["category"] in {"goalGetter", "targetChaser", "briskMinutes", "steppingUp"}
    positions = [reward["position"] for reward in rewards]
    assert positions == sorted(positions), "Rewards must be ordered by position"
    assert len({reward["slug"] for reward in rewards}) == len(rewards), "Reward slugs must be unique"


def test_rewards_detail_matches_list(client, version, require_content):
    rewards = require_content(get_json(client, _path(version)), f"{version} rewards")
    reward = rewards[0]
    detail = get_json(client, _path(version, reward["slug"]))
    assert detail == reward, "Detail and list representations disagree"


def test_rewards_category_filter_is_case_insensitive(client, version, require_content):
    rewards = require_content(get_json(client, _path(version)), f"{version} rewards")
    category = rewards[0]["category"]
    expected = {reward["id"] for reward in rewards if reward["category"].casefold() == category.casefold()}
    for value in (category, category.swapcase()):
        filtered = get_json(client, _path(version), {"category": value})
        assert isinstance(filtered, list)
        assert {reward["id"] for reward in filtered} == expected
        assert all(reward["category"].casefold() == category.casefold() for reward in filtered)


def test_rewards_unknown_category_is_empty(client, version):
    assert get_json(client, _path(version), {"category": f"missing-{uuid4()}"}) == []


def test_rewards_unknown_slug_returns_404(client, version):
    response = client.get(_path(version, f"missing-{uuid4()}"), params={"format": "json"})
    assert_status(response, 404)
    assert isinstance(response.json().get("detail"), str)


@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE"])
def test_rewards_list_rejects_writes(client, version, method):
    response = client.request(method, _path(version), json={}, params={"format": "json"})
    assert_status(response, 405)


@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE"])
def test_rewards_detail_rejects_writes(client, version, method):
    response = client.request(method, _path(version, f"missing-{uuid4()}"), json={}, params={"format": "json"})
    assert_status(response, 405)
