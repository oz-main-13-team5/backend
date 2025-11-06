from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.pills.models import PillItem
from apps.pills.serializers import PillDetailSerializer
from django.shortcuts import get_object_or_404


class PillDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, item_seq):
        pill = get_object_or_404(PillItem, item_seq=item_seq)
        serializer = PillDetailSerializer(pill, context={"request": request})
        return Response(serializer.data, status=200)
