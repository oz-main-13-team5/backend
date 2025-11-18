from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from apps.pills.search_uploads.models import UploadRequest
from apps.pills.search_histories.serilizers import UploadHistorySerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class TenPerPagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({"records": data})

class UploadHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadHistorySerializer
    pagination_class = TenPerPagePagination

    def get_queryset(self):
        return UploadRequest.objects.filter(user=self.request.user).order_by("-created_at")
