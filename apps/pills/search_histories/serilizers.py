from rest_framework import serializers
from apps.pills.search_uploads.models import UploadRequest
from apps.pills.search_histories.utils import map_to_item_seq

class UploadHistorySerializer(serializers.ModelSerializer):
    item_seq = serializers.SerializerMethodField()

    class Meta:
        model = UploadRequest
        fields = ["filename", "url", "status", "item_seq"]

    def get_item_seq(self, obj):
        if obj.status == UploadRequest.Status.COMPLETED:
            return map_to_item_seq(obj.filename)
        return ""