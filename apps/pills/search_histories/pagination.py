from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class TenPerPagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({"records": data})