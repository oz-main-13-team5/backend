from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.uploads.models import UploadRequest
from apps.uploads.serializers import UploadRequestCreateSerializer
from apps.uploads.services.s3_service import S3Uploader


class PillImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    success_message = "이미지를 등록했습니다. 정적으로 찾는 중입니다."

    def _max_upload_size(self) -> int | None:
        return getattr(settings, "UPLOAD_MAX_FILE_SIZE", None)

    def post(self, request):
        serializer = UploadRequestCreateSerializer(
            data=request.data, context={"max_upload_size": self._max_upload_size()}
        )
        if not serializer.is_valid():
            return Response(
                {
                    "error": "입력값이 올바르지 않습니다.",
                    "code": 400,
                    "details": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_obj = serializer.validated_data["file"]
        upload_request = UploadRequest.objects.create(
            user=request.user,
            filename=file_obj.name,
        )

        uploader = S3Uploader()
        content_type = getattr(file_obj, "content_type", None)

        try:
            result = uploader.upload(file_obj, file_obj.name, content_type=content_type)
        except Exception:
            upload_request.mark_failed()
            upload_request.save(update_fields=["status", "completed_at"])
            return Response(
                {
                    "error": "이미지 업로드에 실패했습니다. 잠시 후 다시 시도해주세요.",
                    "code": 500,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        upload_request.url = result.url
        upload_request.save(update_fields=["url"])

        return Response(
            {
                "status": upload_request.status,
                "processed": False,
                "message": self.success_message,
                "image": {
                    "filename": upload_request.filename,
                    "url": upload_request.url,
                },
            },
            status=status.HTTP_200_OK,
        )
