from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Bookmark
from .serializers import BookmarkSerializer
from .services import add_bookmark, remove_bookmark

class BookmarkPagination(PageNumberPagination):
    """
    페이지네이션 설정

    한 페이지에 20개씩 보여줌
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookmarkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related("pill")

    def create(self, request, *args, **kwargs):
        item_seq = request.data.get("item_seq")
        result, code = add_bookmark(request.user, item_seq)
        return Response(result, status=code)

    def destroy(self, request, pk=None):
        result, code = remove_bookmark(request.user, pk)
        return Response(result, status=code)