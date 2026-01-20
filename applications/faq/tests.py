from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from applications.faq.models import Faq


class FaqTests(APITestCase):
    fixtures = ["fixtures.json"]  # noqa: RUF012

    def test_discover(self):
        url = reverse("faq")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), Faq.objects.all().count())

        for faq in response.json():
            pk = faq.get("id")
            f = Faq.objects.get(pk=pk)
            self.assertEqual(pk, f.pk)
            self.assertEqual(faq.get("title"), f.title)
