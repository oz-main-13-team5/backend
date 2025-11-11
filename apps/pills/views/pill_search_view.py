from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from apps.pills.models import PillItem
from apps.pills.serializers import PillSearchSerializer
from apps.pills.services import fetch_pills_from_public_api

PAGE_SIZE_DEFAULT = 20


class PillSearchView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        entp_name = (request.GET.get("entp_name") or "").strip()
        item_name = (request.GET.get("item_name") or "").strip()
        efcy_qesitm = (request.GET.get("efcy_qesitm") or "").strip()
        page = int(request.GET.get("page") or 1)
        page = page if page > 0 else 1
        page_size = PAGE_SIZE_DEFAULT

        if not (entp_name or item_name or efcy_qesitm):
            return Response({"error": "검색 파라미터가 필요합니다", "code": 400}, status=400)

        query = Q()
        if entp_name:
            query &= Q(entp_name__icontains=entp_name)
        if item_name:
            query &= Q(item_name__icontains=item_name)
        if efcy_qesitm:
            query &= Q(efcy_qesitm__icontains=efcy_qesitm)

        print(query)

        pills = PillItem.objects.filter(query)
        total = pills.count()
        offset = (page - 1) * page_size
        pills_page = list(pills[offset: offset + page_size])

        serializer = PillSearchSerializer(
            pills[offset: offset + page_size], many=True, context={"request": request}
        )

        if total == 0:
            try:
                total_external, items = fetch_pills_from_public_api(
                    entp_name=entp_name or None,
                    item_name=item_name or None,
                    efcy_qesitm=efcy_qesitm or None,
                    page=page,
                    page_size=page_size,
                )
                # 저장 (upsert)
                to_create = []
                for it in items:
                    if not it.get("item_seq"):
                        continue
                    exists = PillItem.objects.filter(pk=it["item_seq"]).only("item_seq").exists()
                    if not exists:
                        to_create.append(PillItem(**it))
                if to_create:
                    PillItem.objects.bulk_create(to_create, ignore_conflicts=True)

                # 다시 내부 조회로 정규화된 응답 구성
                queryset = PillItem.objects.filter(query).order_by("item_name", "item_seq")
                total = queryset.count()
                pills_page = list(queryset[offset: offset + page_size])
            except Exception:
                return Response({"error": "공공데이터 조회 중 오류가 발생했습니다", "code": 500}, status=500)

        if total == 0:
            return Response({"error": "검색 결과가 없습니다", "code": 404}, status=404)

        return Response(
            {
                "page": page,
                "total": total,
                "pills": serializer.data,
            },
            status=200,
        )
