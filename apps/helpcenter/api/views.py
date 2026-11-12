from django.contrib.flatpages.models import FlatPage
from rest_framework import permissions, viewsets

from apps.helpcenter.api.serializers import (
    FlatPageSerializer,
    FoireAuxQuestionsSerializer,
    LexiqueSerializer,
)
from apps.helpcenter.models import FoireAuxQuestions, Lexique


class FoireAuxQuestionsApiView(viewsets.ReadOnlyModelViewSet):
    queryset = FoireAuxQuestions.objects.order_by("libelle", "order")
    serializer_class = FoireAuxQuestionsSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["libelle"]


class LexiqueApiView(viewsets.ReadOnlyModelViewSet):
    queryset = Lexique.objects.all()
    serializer_class = LexiqueSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ["title", "definition"]
    ordering_fields = ["title"]


class FlatPageApiView(viewsets.ReadOnlyModelViewSet):
    queryset = FlatPage.objects.filter(registration_required=False)
    serializer_class = FlatPageSerializer
    permission_classes = [permissions.AllowAny]
