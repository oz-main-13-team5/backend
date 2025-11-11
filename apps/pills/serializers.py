from rest_framework import serializers

from apps.pills.models import PillItem
from apps.bookmarks.utils import is_marked_pill


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
        if not request:
            return False
        return is_marked_pill(request.user, obj)


class PillDetailSerializer(serializers.ModelSerializer):
    is_marked = serializers.SerializerMethodField()

    class Meta:
        model = PillItem
        fields = "__all__"

    def get_is_marked(self, obj):
        request = self.context.get("request")
        if not request:
            return False
        return is_marked_pill(request.user, obj)
