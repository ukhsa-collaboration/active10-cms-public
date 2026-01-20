from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from applications.how_it_works.models import HowItWorks


class HowItWorksTests(APITestCase):
    fixtures = ["fixtures.json"]  # noqa: RUF012

    def test_discover(self):
        url = reverse("how_it_works")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), HowItWorks.objects.all().count())

        for hiw in response.json():
            pk = hiw.get("id")
            how_it_works = HowItWorks.objects.get(pk=pk)
            self.assertEqual(pk, how_it_works.pk)
            self.assertEqual(hiw.get("title"), how_it_works.title)
