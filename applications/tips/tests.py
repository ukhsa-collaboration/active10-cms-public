from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from applications.tips.models import MainTip


class TipTests(APITestCase):
    fixtures = ["fixtures.json"]  # noqa: RUF012

    def test_discover(self):
        url = reverse("tips")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), MainTip.objects.all().count())

        for tip in response.json():
            pk = tip.get("id")
            main_tip = MainTip.objects.get(pk=pk)
            self.assertEqual(pk, main_tip.pk)
            self.assertEqual(tip.get("title"), main_tip.title)
