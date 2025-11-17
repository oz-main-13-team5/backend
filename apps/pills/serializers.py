from rest_framework import serializers

from apps.bookmarks.utils import is_marked_pill
from apps.pills.models import PillItem


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
        marked_ids = is_marked_pill(
            getattr(request, "user", None), PillItem.objects.filter(pk=obj.pk)
        )
        return obj.item_seq in marked_ids


class PillSearchSerializer(serializers.ModelSerializer):
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
        marked_ids = self.context.get("marked_ids", set())
        return "true" if obj.item_seq in marked_ids else "false"


class PillDetailSerializer(serializers.ModelSerializer):
    is_marked = serializers.SerializerMethodField()

    class Meta:
        model = PillItem
        fields = "__all__"

    def get_is_marked(self, obj):
        request = self.context.get("request")
        if not request:
            return False
        marked_ids = is_marked_pill(
            getattr(request, "user", None), PillItem.objects.filter(pk=obj.pk)
        )
        return obj.item_seq in marked_ids
