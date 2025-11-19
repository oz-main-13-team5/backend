from rest_framework import serializers
from .models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):
    """
    북마크 조회용 Serializer
    
    북마크 목록을 보여줄 때 사용
    약품 정보도 함께 포함
    """
    
    # 약품 정보 포함 (Nested Serializer)
    # pill_items 테이블의 정보를 포함하여 응답
    item_seq = serializers.CharField(source='pill.item_seq', read_only=True)
    item_name = serializers.CharField(source='pill.item_name', read_only=True)
    entp_name = serializers.CharField(source='pill.entp_name', read_only=True)
    item_image_url = serializers.URLField(
        source='pill.item_image_url',
        read_only=True,
        allow_null=True
    )
    
    class Meta:
        model = Bookmark
        fields = [
            'id',              # 북마크 ID
            'item_seq',        # 약품 품목 기준 코드
            'item_name',       # 약품명 (pill_items 테이블에서)
            'entp_name',       # 제조사명 (pill_items 테이블에서)
            'item_image_url',  # 약품 이미지 URL (pill_items 테이블에서)
        ]
        read_only_fields = ['id', 'item_seq']