from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Bookmark

User = get_user_model()


class BookmarkModelTest(TestCase):
    """북마크 모델 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_bookmark_str(self):
        """북마크 문자열 표현 테스트"""
        # PillItem 모델이 필요하므로 실제 구현 시 추가
        pass


class BookmarkViewTest(TestCase):
    """북마크 API 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_bookmark_list_requires_authentication(self):
        """북마크 목록 조회는 인증이 필요함"""
        response = self.client.get('/bookmark')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_bookmark_list_authenticated(self):
        """인증된 사용자는 북마크 목록 조회 가능"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/bookmark')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

