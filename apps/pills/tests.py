from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.bookmarks.models import Bookmark
from apps.pills.models import PillItem
from django.contrib.auth import get_user_model


User = get_user_model()


class PillBookmarkFlagTests(APITestCase):
    def setUp(self):
        self.pill = PillItem.objects.create(
            item_seq="P001",
            entp_name="테스트제약",
            item_name="테스트약",
            efcy_qesitm="효능",
            use_method_qesitm="사용법",
            atpn_warn_qesitm="주의사항",
            intrc_qesitm="상호작용",
            se_qesitm="부작용",
            deposit_method_qesitm="보관방법",
            item_image_url="http://example.com/image.jpg",
        )
        self.list_url = reverse("pill-list", args=[1])
        self.detail_url = reverse("pill-detail", args=[self.pill.item_seq])

    def test_is_marked_false_for_anonymous(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["pills"][0]["is_marked"])

        detail_response = self.client.get(self.detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertFalse(detail_response.data["is_marked"])

    def test_is_marked_true_when_user_bookmarked(self):
        user = User.objects.create_user(
            email="tester@example.com",
            password="StrongPass123!",
            username="tester@example.com",
        )
        user.is_active = True
        user.save(update_fields=["is_active"])

        Bookmark.objects.create(user=user, pill=self.pill)

        self.client.force_authenticate(user=user)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["pills"][0]["is_marked"])

        detail_response = self.client.get(self.detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertTrue(detail_response.data["is_marked"])
