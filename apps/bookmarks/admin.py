from django.contrib import admin
from .models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """
    북마크 관리자 페이지 설정
    """
    list_display = ['id', 'user', 'item_seq', 'pill']
    list_filter = ['user']
    search_fields = ['user__username', 'item_seq']
    readonly_fields = ['id']
    
    def pill(self, obj):
        """약품명 표시"""
        return obj.pill.item_name if obj.pill else '-'
    pill.short_description = '약품명'

