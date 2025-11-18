from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.pills.search_uploads.models import UploadRequest
from apps.pills.search_uploads.serializers import UploadRequestCreateSerializer, UploadRequestSerializer
from apps.pills.search_uploads.services import S3Uploader


class UploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = UploadRequestCreateSerializer(
            data=request.data,
            context={"max_upload_size": 5 * 1024 * 1024}
        )
        serializer.is_valid(raise_exception=True)
        file_obj = serializer.validated_data["file"]

        upload_request = UploadRequest.objects.create(
            user=request.user,
            filename=file_obj.name,
            status=UploadRequest.Status.PENDING,
        )

        try:
            uploader = S3Uploader()
            content_type = getattr(file_obj, "content_type", "application/octet-stream")
            result = uploader.upload(file_obj, file_obj.name, content_type)

            upload_request.url = result.url
            upload_request.save()

            return Response(
                UploadRequestSerializer(upload_request).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            upload_request.mark_failed()
            upload_request.save()
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
