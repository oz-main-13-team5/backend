from django.contrib.auth import get_user_model
from .models import Bookmark

User = get_user_model()

def user_bookmark_count(user: User) -> int:
    """현재 사용자가 가지고 있는 북마크 개수"""
    return Bookmark.objects.filter(user=user).count()

def get_user_bookmark(user: User, item_seq: str):
    """item_seq로 사용자의 북마크 하나 가져오기"""
    return Bookmark.objects.filter(user=user, pill__item_seq=item_seq).first()

def is_marked_pill(user: User, pill_queryset) -> set[str]:
    """로그인 사용자가 전달된 약 쿼리셋 중 어떤 것들을 북마크했는지 item_seq 집합으로 반환"""
    if not getattr(user, "is_authenticated", False):
        return set()
    pill_ids = list(pill_queryset.values_list("pk", flat=True))
    marked = (
        Bookmark.objects.filter(user=user, pill_id__in=pill_ids)
        .values_list("pill__item_seq", flat=True)
    )
    return set(marked)
