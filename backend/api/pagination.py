from rest_framework.pagination import PageNumberPagination

from constants import Pagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_size = Pagination.page_size.value
