from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, filters
from rest_framework.viewsets import ModelViewSet

from helpcenter.api.serializers import LexiqueSerializer, FoireAuxQuestionsSerializer

from helpcenter.models import Lexique, FoireAuxQuestions

class FoireAuxQuestionsApiView(ModelViewSet):
    serializer_class = FoireAuxQuestionsSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    queryset = FoireAuxQuestions.objects.all()


class LexiqueApiView(ModelViewSet):
    serializer_class = LexiqueSerializer
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
