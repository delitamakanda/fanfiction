from rest_framework.exceptions import ValidationError
from rest_framework.pagination import (
    CursorPagination,
    LimitOffsetPagination,
    PageNumberPagination,
)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class StandardLimitOffsetPagination(LimitOffsetPagination):
    """``?limit=20&offset=40`` pagination, same envelope as before.

    Transition: ``?page=N`` (and ``?page_size=``) are still accepted and
    converted to an offset. A negative, null or non-numeric value is a 400.
    """

    default_limit = 20
    max_limit = 100
    legacy_page_size = 100

    def _int_param(self, request, name, minimum):
        raw = request.query_params.get(name)
        if raw is None or raw == '':
            return None
        try:
            value = int(raw)
        except (TypeError, ValueError):
            value = None
        if value is None or value < minimum:
            raise ValidationError({
                name: [f'Valeur invalide : un entier supérieur ou égal à {minimum} est attendu.'],
            })
        return value

    def _legacy_page(self, request):
        return self._int_param(request, 'page', 1)

    def get_limit(self, request):
        limit = self._int_param(request, self.limit_query_param, 1)
        if limit is None and self._legacy_page(request) is not None:
            limit = self._int_param(request, 'page_size', 1) or self.legacy_page_size
        if limit is None:
            return self.default_limit
        return min(limit, self.max_limit)

    def get_offset(self, request):
        offset = self._int_param(request, self.offset_query_param, 0)
        if offset is not None:
            return offset
        page = self._legacy_page(request)
        if page is not None:
            return (page - 1) * self.get_limit(request)
        return 0

    def get_schema_operation_parameters(self, view):
        params = super().get_schema_operation_parameters(view)
        params.extend([
            {
                'name': 'page', 'required': False, 'in': 'query', 'deprecated': True,
                'description': 'Obsolète : utiliser limit/offset.',
                'schema': {'type': 'integer'},
            },
            {
                'name': 'page_size', 'required': False, 'in': 'query', 'deprecated': True,
                'description': 'Obsolète : utiliser limit.',
                'schema': {'type': 'integer'},
            },
        ])
        return params


class StableCursorPagination(CursorPagination):
    """Cursor pagination on the creation date, with ``id`` as tie-breaker."""

    page_size = 20
    ordering = ('-created', '-id')

    def get_ordering(self, request, queryset, view):
        ordering = list(super().get_ordering(request, queryset, view))
        if not any(field.lstrip('-') in ('id', 'pk') for field in ordering):
            ordering.append('-id' if ordering[0].startswith('-') else 'id')
        return tuple(ordering)


class NotificationCursorPagination(StableCursorPagination):
    pass


class CommentCursorPagination(StableCursorPagination):
    pass
