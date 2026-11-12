from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Default pagination: ``?page=`` and ``?page_size=`` (max 1000)."""

    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000
