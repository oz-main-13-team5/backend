from rest_framework import serializers
from apps.pills.search_uploads.models import UploadRequest

class UploadRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadRequest
        fields = ["id", "filename", "url", "status", "created_at", "completed_at", "item_seq"]
        read_only_fields = fields

class UploadRequestCreateSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        max_size = self.context.get("max_upload_size")
        if max_size and value.size > max_size:
            raise serializers.ValidationError("파일 크기가 허용 범위를 초과했습니다.")
        return value
