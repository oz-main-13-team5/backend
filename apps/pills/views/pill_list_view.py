from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.pills.models import PillItem
from apps.pills.serializers import PillListSerializer


class PillListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, page=1):
        page = int(page)
        limit = 20
        start = (page - 1) * limit
        end = start + limit

        total = PillItem.objects.count()
        pills = PillItem.objects.all()[start:end]
        serializer = PillListSerializer(pills, many=True, context={"request": request})

        return Response(
            {
                "page": page,
                "limit": limit,
                "total": total,
                "pills": serializer.data,
            },
            status=200,
        )
