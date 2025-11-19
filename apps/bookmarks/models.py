from django.db import models
from django.conf import settings
from apps.pills.models import PillItem

class Bookmark(models.Model):
    """
    북마크 모델

    사용자가 즐겨찾기로 등록한 약품 정보를 저장
    테이블 명세서에 정의된 구조를 따름
    """

    # user_id: UUID, FK → users.id
    # 테이블 명세서: user_id는 UUID, NOT NULL, FK → users.id
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # User 모델 (프로젝트 설정에서 가져옴)
        on_delete=models.CASCADE,   # 사용자 삭제 시 북마크도 삭제
        related_name='bookmarks'   # user.bookmarks로 접근 가능
    )

    # item_seq: TEXT, FK → pill_items.item_seq
    # 테이블 명세서: item_seq는 TEXT, NOT NULL, FK → pill_items.item_seq
    pill = models.ForeignKey(
        'pills.PillItem',           # pill_items 테이블 모델
        on_delete=models.CASCADE,   # 약품 삭제 시 북마크도 삭제
        to_field='item_seq',        # item_seq로 연결
        related_name='bookmarked_by' # pill.bookmarked_by로 접근 가능
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        # 같은 사용자가 같은 약품을 중복 북마크하는 것 방지
        # 테이블 명세서에는 명시되지 않았지만, 논리적으로 필요
        unique_together = ('user', 'pill')

        # 최신순으로 정렬 (id가 AUTO_INCREMENT이므로 -id는 최신순)
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.pill.name}"