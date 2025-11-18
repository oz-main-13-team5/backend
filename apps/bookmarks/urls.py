from django.urls import path

from .views import BookmarkView

urlpatterns = [
    # GET /bookmarks/ : 북마크 목록 조회
    # POST /bookmarks/ : 북마크 추가
    # DELETE /bookmarks/ : 북마크 삭제
    path("", BookmarkView.as_view(), name="bookmark"),
]
