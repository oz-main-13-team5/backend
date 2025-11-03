from django.urls import reverse
from rest_framework.test import APITestCase


class TestSignup(APITestCase):
    def test_signup_success(self):
        res = self.client.post(
            reverse("users:REQ_USER_001"),
            {"username": "test@test.com", "password": "12345678"},
        )
        self.assertEqual(res.status_code, 201)
