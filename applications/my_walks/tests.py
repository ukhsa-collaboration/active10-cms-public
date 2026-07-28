from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from applications.my_walks.models import MyWalk, TodayWalk


class MyWalksTests(APITestCase):
    fixtures = ["fixtures.json"]  # noqa: RUF012

    def test_discover(self):
        url = reverse("my_walks")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("my_walks_dynamic_text")), MyWalk.objects.all().count())
        self.assertEqual(len(response.json().get("todays_walks_dynamic_text")), TodayWalk.objects.all().count())

    def test_v1_returns_plain_text(self):
        """v1 stays backward-compatible: each condition maps to a bare text string."""
        response = self.client.get(reverse("my_walks"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        my_walk = MyWalk.objects.first()
        self.assertEqual(response.json()["my_walks_dynamic_text"][my_walk.condition], my_walk.text)


class MyWalksV2Tests(APITestCase):
    fixtures = ["fixtures.json"]

    def test_v2_returns_wheelchair_variant(self):
        """v2: each dynamic-text entry exposes both the walking text and the wheeling
        (wheelchair) variant so the frontend can pick the one for its journey."""
        response = self.client.get(reverse("my_walks_v2"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        my_walks = data["my_walks_dynamic_text"]
        self.assertIsInstance(my_walks, list)
        my_walk = MyWalk.objects.first()
        entry = next(item for item in my_walks if item["condition"] == my_walk.condition)
        self.assertEqual(entry["text"], my_walk.text)
        self.assertEqual(entry["wheelchair_text"], my_walk.wheelchair_text)

        todays = data["todays_walks_dynamic_text"]
        self.assertIsInstance(todays, list)
        target = Target.objects.first()
        today = next(item for item in todays if item["target_name"] == target.target.target_name)
        target_entry = next(t for t in today["target"] if t["condition"] == target.condition)
        self.assertEqual(target_entry["text"], target.text)
        self.assertEqual(target_entry["wheelchair_text"], target.wheelchair_text)