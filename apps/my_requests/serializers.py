from rest_framework import serializers
from .models import ImageSearchRequest
from .utils import map_to_item_seq

class ImageSearchListSerializer(serializers.ModelSerializer):
    item_seq = serializers.SerializerMethodField()

    class Meta:
        model = ImageSearchRequest
        fields = ["filename", "url", "status", "item_seq"]

    def get_item_seq(self, obj):
        if obj.status == "completed":
            return map_to_item_seq(obj.filename)
        return ""