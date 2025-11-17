from apps.bookmarks.models import Bookmark
from apps.pills.models import PillItem


def add_bookmark(user, item_seq: str) -> tuple[dict, int]:
    """
    약품을 북마크에 추가하고 응답 데이터와 HTTP 상태 코드를 반환한다.
    """
    try:
        pill = PillItem.objects.get(item_seq=item_seq)
    except PillItem.DoesNotExist:
        return {"error": "요청한 의약품의 정보가 없습니다.", "code": 404}, 404

    count = Bookmark.objects.filter(user=user).count()
    if count >= 20:
        return {
            "success": False,
            "message": "북마크는 최대 20개까지만 저장할 수 있습니다.",
            "current_count": count,
        }, 201

    exists = Bookmark.objects.filter(user=user, pill=pill).exists()
    if exists:
        return {"error": "이미 북마크에 추가된 약품입니다.", "code": 409}, 409

    Bookmark.objects.create(user=user, pill=pill)
    count = Bookmark.objects.filter(user=user).count()
    return {
        "success": True,
        "message": "약품이 북마크에 추가되었습니다.",
        "current_count": count,
    }, 201


def remove_bookmark(user, item_seq: str) -> tuple[dict, int]:
    """
    약품을 북마크에서 제거하고 응답 데이터와 HTTP 상태 코드를 반환한다.
    """
    bookmark = Bookmark.objects.filter(user=user, pill__item_seq=item_seq).first()
    if bookmark is None:
        return {"error": "요청한 북마크를 찾을 수 없습니다.", "code": 404}, 404

    bookmark.delete()
    count = Bookmark.objects.filter(user=user).count()
    return {
        "success": True,
        "message": "북마크에서 해당 약품이 삭제되었습니다.",
        "current_count": count,
    }, 201
