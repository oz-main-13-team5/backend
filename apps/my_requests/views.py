from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import ImageSearchRequest
from .serializers import ImageSearchListSerializer
from .pagination import TenPerPagePagination

class MyImageSearchListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSearchListSerializer
    pagination_class = TenPerPagePagination

    def get_queryset(self):
        return ImageSearchRequest.objects.filter(user=self.request.user).order_by("-created_at")