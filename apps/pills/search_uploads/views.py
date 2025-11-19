import os
import uuid
import logging
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.pills.search_uploads.models import UploadRequest
from apps.pills.search_uploads.serializers import UploadRequestCreateSerializer, UploadRequestSerializer
from apps.pills.search_uploads.services import S3Uploader

log = logging.getLogger(__name__)

class UploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = UploadRequestCreateSerializer(
            data=request.data,
            context={"max_upload_size": 5 * 1024 * 1024}
        )
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                {"error": "파일 검증 실패", "detail": str("파일 검증 실패")},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_obj = serializer.validated_data.get("file")
        if not file_obj:
            return Response(
                {"error": "파일이 제출되지 않았습니다", "detail": "form-data에서 key=file 로 파일을 제출해야 합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 파일명 생성
        safe_filename = f"{uuid.uuid4().hex}{os.path.splitext(file_obj.name)[1]}"

        upload_request = UploadRequest.objects.create(
            user=request.user,
            filename=file_obj.name,
            status=UploadRequest.Status.PENDING,
        )

        try:
            uploader = S3Uploader()
            content_type = getattr(file_obj, "content_type", "application/octet-stream")
            result = uploader.upload(file_obj, safe_filename, content_type)

            # URL만 저장, 상태는 PENDING 유지
            upload_request.url = result.url
            upload_request.save()

            return Response(
                UploadRequestSerializer(upload_request).data,
                status=status.HTTP_201_CREATED
            )

        except RuntimeError as e:
            # 환경 변수 설정 문제
            upload_request.mark_failed()
            upload_request.save()
            return Response(
                {"error": "S3 설정 오류", "detail": str("S3 설정 오류(RuntimeError)")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            # boto3나 기타 예외
            log.exception("S3 업로드 실패")
            upload_request.mark_failed()
            upload_request.save()
            return Response(
                {"error": "업로드 실패", "detail": str("boto3 업로드 실패")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
