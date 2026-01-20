from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from applications.discover.models import Cta, Discover, SplashScreen, Tip


class DiscoverTests(APITestCase):
    fixtures = ["fixtures.json"]  # noqa: RUF012

    def test_discover(self):
        url = reverse("discover")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("discover")), Discover.objects.all().count())
        self.assertEqual(len(response.json().get("tips")), Tip.objects.all().count())

        for discover in response.json().get("discover"):
            splash_screen = discover.get("splash_screen")
            if splash_screen:
                pk = splash_screen.get("id")
                ss = SplashScreen.objects.get(pk=pk)

                self.assertEqual(pk, ss.pk)
                self.assertEqual(splash_screen.get("title"), ss.title)

        for tip in response.json().get("tips"):
            cta = tip.get("cta")
            if cta:
                pk = cta.get("id")
                c = Cta.objects.get(pk=pk)

                self.assertEqual(pk, c.pk)
                self.assertEqual(cta.get("button"), c.button)
