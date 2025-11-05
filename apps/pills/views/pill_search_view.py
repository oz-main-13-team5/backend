from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from apps.pills.models import PillItem
from apps.pills.serializers import PillListSerializer


class PillSearchView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, keyword, page=1):
        page = int(page)
        query = (
            Q(entp_name__icontains=keyword) |
            Q(item_name__icontains=keyword) |
            Q(efcy_qesitm__icontains=keyword)
        )

        pills = PillItem.objects.filter(query)

        limit = 20
        total = pills.count()
        start = (page - 1) * limit
        end = start + limit

        serializer = PillListSerializer(
            pills[start:end], many=True, context={"request": request}
        )

        return Response(
            {
                "keyword": keyword,
                "page": page,
                "total": total,
                "pills": serializer.data,
            },
            status=200
        )
