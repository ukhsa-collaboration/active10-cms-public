import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from applications.goals.models import Goal


class GoalTests(APITestCase):
    fixtures = ["fixtures.json"]  # noqa: RUF012

    def test_get_goal(self):
        url = reverse("goals")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), Goal.objects.all().count())

    def test_create_goal(self):
        url = reverse("goals")
        device_id = str(uuid.uuid4())
        data = {"text": "be better than yesterday", "user": device_id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = f"{reverse('goals')}?user={device_id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), Goal.objects.all().count())

        for goal in response.json():
            user = goal.get("user")
            if user:
                self.assertEqual(user, device_id)
