from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.pills.models import PillItem
from apps.pills.serializers import PillListSerializer
from math import ceil

class PillListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, page=1):
        page_param = request.GET.get("page", "1")
        try:
            page = int(page_param)
        except ValueError:
            # page=abc 같은 경우도 404 처리
            return Response(
                {"error": "데이터가 없습니다", "code": 404},
                status=404
            )

        if page < 1:
            return Response(
                {"error": "데이터가 없습니다", "code": 404},
                status=404
            )

        limit = 20
        total = PillItem.objects.count()

        if total == 0:
            total_pages = 1
        else:
            total_pages = ceil(total / limit)

        if page > total_pages:
            return Response(
                {"error": "데이터가 없습니다", "code": 404},
                status=404
            )

        start = (page - 1) * limit
        end = start + limit
        pills = PillItem.objects.all()[start:end]
        serializer = PillListSerializer(pills, many=True, context={"request": request})

        return Response(
            {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages,
                "pills": serializer.data,
            },
            status=200,
        )
