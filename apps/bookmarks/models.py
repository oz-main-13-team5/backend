from django.db import models
from django.conf import settings

class Bookmark(models.Model):
    """
    북마크 모델
    
    사용자가 즐겨찾기로 등록한 약품 정보를 저장
    테이블 명세서에 정의된 구조를 따름
    """
    
    # id: INT, AUTO_INCREMENT (PK)
    # 테이블 명세서: id는 INT, PRIMARY KEY, AUTO_INCREMENT
    id = models.AutoField(primary_key=True)
    
    # user_id: UUID, FK → users.id
    # 테이블 명세서: user_id는 UUID, NOT NULL, FK → users.id
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # User 모델 (프로젝트 설정에서 가져옴)
        on_delete=models.CASCADE,   # 사용자 삭제 시 북마크도 삭제
        related_name='bookmarks',   # user.bookmarks로 접근 가능
        db_column='user_id'         # DB 컬럼명: user_id (테이블 명세서와 일치)
    )
    
    # item_seq: TEXT, FK → pill_items.item_seq
    # 테이블 명세서: item_seq는 TEXT, NOT NULL, FK → pill_items.item_seq
    pill = models.ForeignKey(
        'pills.PillItem',           # pill_items 테이블 모델
        on_delete=models.CASCADE,   # 약품 삭제 시 북마크도 삭제
        to_field='item_seq',        # item_seq로 연결
        related_name='bookmarked_by', # pill.bookmarked_by로 접근 가능
        db_column='item_seq'       # DB 컬럼명: item_seq (테이블 명세서와 일치)
    )
    
    class Meta:
        db_table = 'bookmark'  # 테이블명: bookmark (테이블 명세서와 일치)
        
        # 같은 사용자가 같은 약품을 중복 북마크하는 것 방지
        # 테이블 명세서에는 명시되지 않았지만, 논리적으로 필요
        unique_together = ('user', 'pill')
        
        # 최신순으로 정렬 (id가 AUTO_INCREMENT이므로 -id는 최신순)
        ordering = ['-id']
    
    @property
    def item_seq(self):
        """데이터베이스 컬럼명(item_seq)과 필드명(pill) 간의 호환을 위한 helper"""
        return self.pill_id
    
    def __str__(self):
        """관리자 페이지에서 보기 좋게 표시"""
        try:
            return f"{self.user.username} - {self.pill.item_name}"
        except:
            return f"{self.user.username} - {self.item_seq}"
