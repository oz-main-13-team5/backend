from rest_framework import serializers
from apps.pills.models import PillItem


class PillListSerializer(serializers.ModelSerializer):
    is_marked = serializers.SerializerMethodField()

    class Meta:
        model = PillItem
        fields = ["item_seq", "item_name", "efcy_qesitm", "entp_name", "item_image_url"]

class PillSearchSerializer(serializers.ModelSerializer):
    is_marked = serializers.SerializerMethodField()

    class Meta:
        model = PillItem
        fields = ["item_seq", "item_name", "efcy_qesitm", "entp_name", "item_image_url", "is_marked"]

    def get_is_marked(self, obj):
        marked_ids = self.context.get("marked_ids", set())
        return "true" if obj.item_seq in marked_ids else "false"

class PillDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PillItem
        fields = "__all__"
