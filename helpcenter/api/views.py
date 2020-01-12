from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions, filters

from helpcenter.api.serializers import LexiqueSerializer, FoireAuxQuestionsSerializer

from helpcenter.models import Lexique, FoireAuxQuestions

class FoireAuxQuestionsApiView(generics.ListAPIView):
    serializer_class = FoireAuxQuestionsSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )
    queryset = FoireAuxQuestions.objects.all()


class LexiqueApiView(generics.ListAPIView):
    serializer_class = LexiqueSerializer
    pagination_class = None
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
        'created',
        'updated',
    )
    ordering = (
        'title',
    )
    search_fields = (
        'title',
        'definition',
    )
    queryset = Lexique.objects.all()