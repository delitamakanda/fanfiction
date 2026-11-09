from django.db import connection
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend

SEARCH_MIN_LENGTH = 2
SEARCH_MAX_LENGTH = 100
SEARCH_CONFIG = 'simple'  # no stemming: the content is bilingual
TRIGRAM_THRESHOLD = 0.3


class FanficSearchFilter(BaseFilterBackend):
    """``?search=`` full-text search on fanfics.

    PostgreSQL: weighted ``SearchVector`` (GIN index), ranked by relevance and
    tolerant to typos through ``pg_trgm``. Other engines (SQLite): ``icontains``.
    Must be applied on a queryset that is already restricted to the fanfics the
    user may see.
    """

    search_param = 'search'

    def get_search_term(self, request):
        term = request.query_params.get(self.search_param, '').strip()
        if not term:
            return ''
        if len(term) < SEARCH_MIN_LENGTH:
            raise ValidationError({
                self.search_param: [
                    f'La recherche doit contenir au moins {SEARCH_MIN_LENGTH} caractères.'],
            })
        return term[:SEARCH_MAX_LENGTH]

    def filter_queryset(self, request, queryset, view):
        term = self.get_search_term(request)
        if not term:
            return queryset
        if connection.vendor == 'postgresql':
            return self.filter_postgres(request, queryset, term)
        return self.filter_generic(queryset, term)

    @staticmethod
    def filter_generic(queryset, term):
        condition = Q()
        for word in term.split():
            condition &= (
                Q(title__icontains=word)
                | Q(synopsis__icontains=word)
                | Q(description__icontains=word)
                | Q(author__username__icontains=word)
            )
        return queryset.filter(condition)

    @staticmethod
    def filter_postgres(request, queryset, term):
        from django.contrib.postgres.search import (
            SearchQuery,
            SearchRank,
            SearchVector,
            TrigramSimilarity,
        )

        vector = (
            SearchVector('title', weight='A', config=SEARCH_CONFIG)
            + SearchVector('synopsis', weight='B', config=SEARCH_CONFIG)
            + SearchVector('description', weight='C', config=SEARCH_CONFIG)
        )
        query = SearchQuery(term, config=SEARCH_CONFIG, search_type='plain')
        queryset = queryset.annotate(
            search_rank=SearchRank(vector, query),
            title_similarity=TrigramSimilarity('title', term),
        ).filter(
            Q(search_rank__gt=0)
            | Q(title_similarity__gt=TRIGRAM_THRESHOLD)
            | Q(author__username__icontains=term)
        )
        if not request.query_params.get('ordering'):
            queryset = queryset.order_by('-search_rank', '-title_similarity', '-publish', '-id')
        return queryset
