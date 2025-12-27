from django.contrib.flatpages.models import FlatPage
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters, viewsets

from api import custompagination
from helpcenter.api.serializers import FlatPageSerializer, LexiqueSerializer, FoireAuxQuestionsSerializer
from helpcenter.models import Lexique, FoireAuxQuestions


class FoireAuxQuestionsApiView(viewsets.ModelViewSet):
    serializer_class = FoireAuxQuestionsSerializer
    pagination_class = custompagination.StandardResultsSetPagination
    permission_classes = (
        permissions.AllowAny,
    )
    queryset = FoireAuxQuestions.objects.all()
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        cache_key = 'foire_aux_questions_api_view'
        qs = cache.get(cache_key)
        if qs is None:
            qs = FoireAuxQuestions.objects.all()
            cache.set(cache_key, qs, 60 * 60 * 24)
        return super().list(request, *args, **kwargs)

class LexiqueApiView(viewsets.ModelViewSet):
    serializer_class = LexiqueSerializer
    pagination_class = custompagination.StandardResultsSetPagination
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    permission_classes = (
        permissions.AllowAny,
    )
    ordering_fields = (
        'title',
    )
    search_fields = (
        'definition',
    )
    queryset = Lexique.objects.all()
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        cache_key = 'lexique_api_view'
        qs = cache.get(cache_key)
        if qs is None:
            qs = Lexique.objects.all()
            cache.set(cache_key, qs, 60 * 60 * 24)
        return super().list(request, *args, **kwargs)


class FlatPageApiView(viewsets.ModelViewSet):
    queryset = FlatPage.objects.all()
    serializer_class = FlatPageSerializer
    pagination_class = custompagination.StandardResultsSetPagination
    permission_classes = (
        permissions.AllowAny,
    )
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        cache_key = 'flatpages_api_view'
        qs = cache.get(cache_key)
        if qs is None:
            qs = FlatPage.objects.all()
            cache.set(cache_key, qs, 60 * 60 * 24)
        return super().list(request, *args, **kwargs)
