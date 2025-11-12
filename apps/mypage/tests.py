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
        self.nickname_url = reverse("my-page-nickname")
        self.password_url = reverse("my-page-password")

    def test_get_profile(self):
        response = self.client.get(reverse("my-page"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.email)
        self.assertEqual(response.data["nickname"], self.user.nickname)

    def test_update_nickname(self):
        response = self.client.patch(self.nickname_url, {"nickname": "새닉네임"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, "새닉네임")

    def test_update_password_success(self):
        payload = {
            "current_password": "StrongPass123!",
            "new_password": "NewPass123!",
        }
        response = self.client.patch(self.password_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPass123!"))

    def test_update_password_wrong_current(self):
        payload = {
            "current_password": "WrongPass!",
            "new_password": "NewPass123!",
        }
        response = self.client.patch(self.password_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
