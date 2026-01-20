from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class DiscoverTests(APITestCase):
    fixtures = ["fixtures.json"]  # noqa: RUF012

    def test_discover(self):
        url = reverse("tips")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
