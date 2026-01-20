from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from applications.about_one_you.models import AboutOneYou, Application


class AboutOneYouTests(APITestCase):
    fixtures = ["fixtures.json"]  # noqa: RUF012

    def test_about_one_you(self):
        url = reverse("about_one_you")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("apps")), Application.objects.all().count())
        self.assertEqual(response.json().get("about").get("text"), AboutOneYou.objects.first().text)
