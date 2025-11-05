from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Bookmark
from .serializers import (
    BookmarkSerializer, 
    BookmarkCreateSerializer, 
    BookmarkDeleteSerializer
)
# ⚠️ PillItem 모델 위치에 맞게 수정
from apps.pills.models import PillItem

class BookmarkPagination(PageNumberPagination):
    """
    페이지네이션 설정
    
    한 페이지에 20개씩 보여줌
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookmarkView(APIView):
    """
    북마크 조회/추가/삭제
    
    GET: 북마크 목록 조회
    POST: 북마크 추가
    DELETE: 북마크 삭제
    """
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능
    pagination_class = BookmarkPagination
    
    def get(self, request):
        """
        북마크 목록 조회
        
        1. 현재 로그인한 사용자의 북마크만 조회
        2. 약품 정보도 함께 조회 (select_related로 성능 최적화)
        3. 페이지네이션 적용
        
        TODO: 페이지네이션 응답 구조는 프론트엔드와 협의 후 조정
        """
        # 현재 로그인한 사용자의 북마크만 조회
        bookmarks = Bookmark.objects.filter(
            user=request.user
        ).select_related('pill')  # 약품 정보도 함께 가져오기 (성능 최적화)
        
        # 페이지네이션
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(bookmarks, request)
        
        if page is not None:
            # 페이지네이션된 응답
            serializer = BookmarkSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # 페이지네이션 없이 전체 반환
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """북마크 추가 (20개 제한 및 중복 방지 포함)"""
        # 입력 데이터 검증
        serializer = BookmarkCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "error": "입력값이 올바르지 않습니다.",
                "code": 400
            }, status=status.HTTP_400_BAD_REQUEST)
        
        item_seq = serializer.validated_data['item_seq']
        
        # 약품 정보 조회 (pill_items 테이블)
        try:
            pill = PillItem.objects.get(item_seq=item_seq)
        except PillItem.DoesNotExist:
            return Response({
                "error": "요청한 의약품의 정보가 없습니다.",
                "code": 404
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 현재 북마크 개수 (중복/제한 체크를 위해 선조회)
        current_count = Bookmark.objects.filter(user=request.user).count()
        
        # 20개 제한 체크
        if current_count >= 20:
            return Response({
                "success": False,
                "message": "북마크는 최대 20개까지만 저장할 수 있습니다.",
                "current_count": current_count
            }, status=status.HTTP_201_CREATED)  # 명세서 기준 201 유지
        
        # 중복 체크
        if Bookmark.objects.filter(user=request.user, pill=pill).exists():
            return Response({
                "error": "이미 북마크에 추가된 약품입니다.",
                "code": 409
            }, status=status.HTTP_409_CONFLICT)
        
        # 북마크 생성
        Bookmark.objects.create(user=request.user, pill=pill)
        current_count += 1
        
        # 응답 (명세서 기준)
        return Response({
            "success": True,
            "message": "약품이 북마크에 추가되었습니다.",
            "current_count": current_count
        }, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        """
        북마크 삭제
        
        1. body에서 id 받음 (명세서 기준)
        2. 북마크 조회 (본인 것만)
        3. 삭제
        """
        # 입력 데이터 검증
        serializer = BookmarkDeleteSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "error": "입력값이 올바르지 않습니다.",
                "code": 400
            }, status=status.HTTP_400_BAD_REQUEST)
        
        bookmark_id = serializer.validated_data['id']
        
        # 본인의 북마크만 삭제 가능
        try:
            bookmark = Bookmark.objects.get(
                id=bookmark_id, 
                user=request.user  # 본인 것만 삭제 가능
            )
            bookmark.delete()
        except Bookmark.DoesNotExist:
            return Response({
                "error": "요청한 북마크를 찾을 수 없습니다.",
                "code": 404
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 삭제 후 남은 개수 반환
        current_count = Bookmark.objects.filter(user=request.user).count()
        return Response({
            "success": True,
            "message": "북마크에서 해당 약품이 삭제되었습니다.",
            "current_count": current_count
        }, status=status.HTTP_201_CREATED)  # 명세서 기준 201 반환
