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
        self.assertEqual(
            len(response.json().get("my_walks_dynamic_text")),
            MyWalk.objects.all().count(),
        )
        self.assertEqual(
            len(response.json().get("todays_walks_dynamic_text")),
            TodayWalk.objects.all().count(),
        )
