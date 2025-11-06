from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Bookmark
from apps.pills.models import PillItem

User = get_user_model()


class BookmarkModelTest(TestCase):
    """북마크 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
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

    def test_bookmark_str(self):
        bookmark = Bookmark.objects.create(user=self.user, pill=self.pill)
        self.assertIn(self.pill.item_name, str(bookmark))
        self.assertIn(self.user.username, str(bookmark))


class BookmarkViewTest(TestCase):
    """북마크 API 테스트"""
    
    def setUp(self):
        self.url = reverse("bookmark")
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
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
    
    def test_bookmark_list_requires_authentication(self):
        """북마크 목록 조회는 인증이 필요함"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_bookmark_list_authenticated(self):
        """인증된 사용자는 북마크 목록 조회 가능"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bookmark_add_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {"item_seq": self.pill.item_seq}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["current_count"], 1)

    def test_bookmark_add_duplicate_returns_409(self):
        Bookmark.objects.create(user=self.user, pill=self.pill)
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {"item_seq": self.pill.item_seq}, format="json")

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("이미 북마크에 추가된 약품입니다.", response.data["error"])

    def test_bookmark_add_over_limit_returns_success_false(self):
        for idx in range(20):
            pill = PillItem.objects.create(
                item_seq=f"P{idx+10:03}",
                entp_name="제약사",
                item_name=f"약품{idx}",
                efcy_qesitm="효능",
                use_method_qesitm="사용법",
                atpn_warn_qesitm="주의사항",
                intrc_qesitm="상호작용",
                se_qesitm="부작용",
                deposit_method_qesitm="보관방법",
                item_image_url="http://example.com/image.jpg",
            )
            Bookmark.objects.create(user=self.user, pill=pill)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {"item_seq": self.pill.item_seq}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["current_count"], 20)

    def test_bookmark_delete(self):
        bookmark = Bookmark.objects.create(user=self.user, pill=self.pill)
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.url, {"id": bookmark.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
