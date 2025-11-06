from rest_framework import serializers
from apps.pills.models import PillItem


class PillListSerializer(serializers.ModelSerializer):
    is_marked = serializers.SerializerMethodField()

    class Meta:
        model = PillItem
        fields = ["item_seq", "item_name", "efcy_qesitm", "entp_name", "item_image_url"]


class PillDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PillItem
        fields = "__all__"
