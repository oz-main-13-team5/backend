from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class UserProfileViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester@example.com",
            email="tester@example.com",
            password="StrongPass123!",
            nickname="테스터",
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        response = self.client.get(reverse("my-page"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.email)
        self.assertEqual(response.data["nickname"], self.user.nickname)

    def test_update_nickname(self):
        response = self.client.patch(reverse("my-page"), {"nickname": "새닉네임"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("nickname", response.data["updated_fields"])

    def test_update_password_requires_min_length(self):
        response = self.client.patch(reverse("my-page"), {"password": "short"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

