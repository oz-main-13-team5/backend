from django.urls import path
from .views import BookmarkView

urlpatterns = [
    # GET /bookmark: 북마크 목록 조회
    # POST /bookmark: 북마크 추가
    # DELETE /bookmark: 북마크 삭제
    path('bookmark', BookmarkView.as_view(), name='bookmark'),
]

