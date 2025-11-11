from django.contrib.auth import get_user_model
from .models import Bookmark

User = get_user_model()

def user_bookmark_count(user: User) -> int:
    """현재 사용자가 가지고 있는 북마크 개수"""
    return Bookmark.objects.filter(user=user).count()

def get_user_bookmark(user: User, item_seq: str):
    """item_seq로 사용자의 북마크 하나 가져오기"""
    return Bookmark.objects.filter(user=user, pill__item_seq=item_seq).first()

def is_marked_pill(user: User, pill) -> bool:
    """로그인 사용자가 해당 약을 북마크했는지 여부"""
    if not getattr(user, "is_authenticated", False):
        return False
    return Bookmark.objects.filter(user=user, pill=pill).exists()
