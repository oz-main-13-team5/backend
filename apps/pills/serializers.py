from rest_framework import serializers

from apps.pills.models import PillItem
from apps.bookmarks.models import Bookmark


class PillListSerializer(serializers.ModelSerializer):
    is_marked = serializers.SerializerMethodField()

    class Meta:
        model = PillItem
        fields = [
            "item_seq",
            "item_name",
            "efcy_qesitm",
            "entp_name",
            "item_image_url",
            "is_marked",
        ]

    def get_is_marked(self, obj):
        request = self.context.get("request")
        if not request or not hasattr(request, "user") or not request.user.is_authenticated:
            return False
        return Bookmark.objects.filter(user=request.user, pill=obj).exists()


class PillDetailSerializer(serializers.ModelSerializer):
    is_marked = serializers.SerializerMethodField()

    class Meta:
        model = PillItem
        fields = "__all__"

    def get_is_marked(self, obj):
        request = self.context.get("request")
        if not request or not hasattr(request, "user") or not request.user.is_authenticated:
            return False
        return Bookmark.objects.filter(user=request.user, pill=obj).exists()
